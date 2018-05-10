from django.db import models
from django.utils.translation import ugettext_lazy as _
from hello_uptime.utils import MonitoringInterval, MonitorStatus


class Monitor(models.Model):
    url = models.URLField(verbose_name=_("URL"), unique=True)
    interval = models.PositiveSmallIntegerField(
        verbose_name=_("Monitoring interval"), choices=MonitoringInterval.get_choices(),
        default=MonitoringInterval.get_default())
    status = models.CharField(verbose_name=_("Status"), max_length=9, choices=MonitorStatus.get_choices(), blank=True)
    is_active = models.BooleanField(verbose_name=_("Is active?"), blank=True, default=True)
    checked_at = models.DateTimeField(verbose_name=_("Checked at"), null=True, editable=False)
    created_at = models.DateTimeField(verbose_name=_("Created at"), auto_now_add=True)

    class Meta:
        verbose_name = _("Monitor")
        verbose_name_plural = _("Monitors")
        ordering = ('-created_at',)

    def __str__(self):
        return self.url
