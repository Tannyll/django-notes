import requests
from django.core.management.base import BaseCommand
from django.utils import timezone
from requests.exceptions import SSLError

from hello_uptime.models import Monitor
from hello_uptime.utils import MonitorStatus


class Command(BaseCommand):
    help = "Checks the urls for monitors"

    def add_arguments(self, parser):
        parser.add_argument('urls', nargs='+', type=str)

    def handle(self, *args, **options):
        urls = options['urls']

        for url in urls:
            monitors = Monitor.objects.filter(is_active=True, url=url)
            self.stdout.write(self.style.WARNING("{} - {} monitor(s)".format(url, monitors.count())), ending=': ')

            try:
                response = requests.get(url)
                status = MonitorStatus.ONLINE if response.status_code == 200 else MonitorStatus.OFFLINE
            except SSLError:
                status = MonitorStatus.OFFLINE

            monitors.update(status=status, checked_at=timezone.now())
            status_style = self.style.ERROR if status == MonitorStatus.OFFLINE else self.style.SUCCESS
            self.stdout.write(status_style(status))
