import argparse

from django.core.management.base import BaseCommand

from hello_uptime.models import Monitor
from hello_uptime.utils import MonitorStatus


class Command(BaseCommand):
    help = "Checks the urls for monitors"

    def add_arguments(self, parser):
        parser.add_argument('urls', nargs=argparse.ZERO_OR_MORE, type=str)

    def handle(self, *args, **options):
        for url in Monitor.objects.get_available_urls(urls=options['urls']):
            status, monitors = Monitor.objects.check_url(url)
            self.stdout.write(self.style.WARNING("{} - {} monitor(s)".format(url, monitors.count())), ending=': ')

            status_style = self.style.ERROR if status == MonitorStatus.OFFLINE else self.style.SUCCESS
            self.stdout.write(status_style(status))
