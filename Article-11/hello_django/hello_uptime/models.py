import requests
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from hello_uptime.utils import MonitoringInterval, MonitorStatus


class MonitorManager(models.Manager):
    def get_available_monitors(self, urls=None):
        urls = urls or []  # it should be a list
        now = timezone.now()
        available_monitors = self.filter(is_active=True).filter(
            models.Q(checked_at__isnull=True) |
            models.Q(interval=MonitoringInterval.MIN_5,
                     checked_at__lt=now - relativedelta(seconds=MonitoringInterval.MIN_5)) |
            models.Q(interval=MonitoringInterval.MIN_30,
                     checked_at__lt=now - relativedelta(seconds=MonitoringInterval.MIN_30)) |
            models.Q(interval=MonitoringInterval.HOUR_1,
                     checked_at__lt=now - relativedelta(seconds=MonitoringInterval.HOUR_1)) |
            models.Q(interval=MonitoringInterval.HOUR_6,
                     checked_at__lt=now - relativedelta(seconds=MonitoringInterval.HOUR_6)))
        if urls:
            available_monitors = available_monitors.filter(monitor_url__in=urls)
        return available_monitors

    def get_available_urls(self, urls=None):
        available_monitors = self.get_available_monitors(urls=urls)
        return available_monitors.values_list('monitor_url', flat=True).distinct().order_by('monitor_url')

    def check_url(self, url):
        try:
            response = requests.get(url)
            status = MonitorStatus.ONLINE if response.status_code == 200 else MonitorStatus.OFFLINE
        except (requests.exceptions.SSLError, requests.exceptions.ConnectionError):
            status = MonitorStatus.OFFLINE
        monitors = self.filter(is_active=True, monitor_url=url)
        monitors.update(status=status, checked_at=timezone.now())
        return status, monitors


class Monitor(models.Model):
    user = models.ForeignKey(
        verbose_name=_("User"), to=settings.AUTH_USER_MODEL, related_name='monitors', on_delete=models.CASCADE,
        null=True)
    monitor_url = models.URLField(verbose_name=_("URL"))
    interval = models.PositiveSmallIntegerField(
        verbose_name=_("Monitoring interval"), choices=MonitoringInterval.get_choices(),
        default=MonitoringInterval.get_default())
    status = models.CharField(verbose_name=_("Status"), max_length=9, choices=MonitorStatus.get_choices(), blank=True)
    is_active = models.BooleanField(verbose_name=_("Is active?"), blank=True, default=True)
    checked_at = models.DateTimeField(verbose_name=_("Checked at"), null=True, editable=False)
    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    objects = MonitorManager()

    class Meta:
        verbose_name = _("Monitor")
        verbose_name_plural = _("Monitors")
        ordering = ('-created_at',)
        unique_together = ('user', 'monitor_url')

    def __str__(self):
        return self.monitor_url
