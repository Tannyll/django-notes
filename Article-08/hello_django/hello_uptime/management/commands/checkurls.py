import requests

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.core.validators import URLValidator
from requests.exceptions import SSLError

from hello_uptime.models import Monitor
from hello_uptime.utils import MonitorStatus


class Command(BaseCommand):
    help = "Checks the urls for monitors"

    def add_arguments(self, parser):
        parser.add_argument('urls', nargs='+', type=str)

    def handle(self, *args, **options):
        valid_urls, invalid_urls = self.get_urls(options)

        if not valid_urls:
            self.stderr.write(self.style.ERROR("There's no valid urls, please check again."))
            return

        if invalid_urls:
            self.stderr.write(self.style.ERROR("We passed these invalid urls:"))
            for invalid_url in invalid_urls:
                self.stderr.write(self.style.ERROR("\t- {}".format(invalid_url)))

        for url in valid_urls:
            monitors = Monitor.objects.filter(is_active=True, url=url)
            self.stdout.write(self.style.WARNING("{} - {} monitor(s)".format(url, monitors.count())), ending=': ')
            if not monitors.exists():
                self.stdout.write(self.style.WARNING("passed"))
                continue

            try:
                response = requests.get(url)
                status = MonitorStatus.ONLINE if response.status_code == 200 else MonitorStatus.OFFLINE
            except SSLError:
                status = MonitorStatus.OFFLINE

            monitors.update(status=status)
            status_style = self.style.ERROR if status == MonitorStatus.OFFLINE else self.style.SUCCESS
            self.stdout.write(status_style(status))

    def get_urls(self, options):
        urls = options['urls']
        valid_urls = []
        invalid_urls = []
        validate_url = URLValidator(schemes=['http', 'https'])

        for url in urls:
            try:
                validate_url(url)
            except ValidationError:
                invalid_urls.append(url)
            else:
                valid_urls.append(url)

        return valid_urls, invalid_urls
