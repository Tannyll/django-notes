import argparse

import requests
from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db import models
from django.utils import timezone
from requests.exceptions import SSLError

from hello_uptime.models import Monitor
from hello_uptime.utils import MonitorStatus, MonitoringInterval


class Command(BaseCommand):
    help = "Checks the urls for monitors"

    def add_arguments(self, parser):
        parser.add_argument('urls', nargs=argparse.ZERO_OR_MORE, type=str)
        parser.add_argument('--mail_clients', action='store_true', dest='mail_clients')

    def handle(self, *args, **options):
        now = timezone.now()
        offline_urls = []
        available_monitors = Monitor.objects.filter(is_active=True).filter(
            models.Q(interval=MonitoringInterval.MIN_5,
                     checked_at__lt=now - relativedelta(seconds=MonitoringInterval.MIN_5)) |
            models.Q(interval=MonitoringInterval.MIN_30,
                     checked_at__lt=now - relativedelta(seconds=MonitoringInterval.MIN_30)) |
            models.Q(interval=MonitoringInterval.HOUR_1,
                     checked_at__lt=now - relativedelta(seconds=MonitoringInterval.HOUR_1)) |
            models.Q(interval=MonitoringInterval.HOUR_6,
                     checked_at__lt=now - relativedelta(seconds=MonitoringInterval.HOUR_6)))

        urls = options['urls']
        if urls:
            available_monitors = available_monitors.filter(url__in=urls)
        urls = available_monitors.values_list('url', flat=True).distinct().order_by('url')

        for url in urls:
            monitors = Monitor.objects.filter(is_active=True, url=url)
            self.stdout.write(self.style.WARNING("{} - {} monitor(s)".format(url, monitors.count())), ending=': ')

            try:
                response = requests.get(url)
                status = MonitorStatus.ONLINE if response.status_code == 200 else MonitorStatus.OFFLINE
            except SSLError:
                status = MonitorStatus.OFFLINE

            monitors.update(status=status, checked_at=now)
            status_style = self.style.ERROR if status == MonitorStatus.OFFLINE else self.style.SUCCESS
            self.stdout.write(status_style(status))

            if status == MonitorStatus.OFFLINE:
                offline_urls.append(url)

        if options['mail_clients'] and offline_urls:
            for url in offline_urls:
                self.mail_clients(url, available_monitors)

    def mail_clients(self, url, available_monitors):
        subject = "[Hello Uptime] Monitor is DOWN: {}".format(url)
        for monitor in available_monitors.filter(url=url, user__isnull=False):
            message_list = [
                "Hi {},".format(monitor.user.get_full_name()),
                "The monitor ({}) is currently DOWN.".format(url),
            ]
            send_mail(
                subject, '\n'.join(message_list), from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[monitor.user.email])
