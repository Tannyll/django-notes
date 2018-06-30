from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.mail import send_mail

from hello_uptime.models import Monitor
from hello_uptime.utils import MonitorStatus

logger = get_task_logger('hello_uptime.tasks')


@shared_task
def send_mail_to_client(url):
    subject = "[Hello Uptime] Monitor is DOWN: {}".format(url)
    monitors = Monitor.objects.get_available_monitors(urls=[url])
    for monitor in monitors:
        message_list = [
            "Hi {},".format(monitor.user.get_full_name()),
            "The monitor ({}) is currently DOWN.".format(url),
        ]
        send_mail(
            subject, '\n'.join(message_list), from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[monitor.user.email])


@shared_task
def check_monitors():
    urls = Monitor.objects.get_available_urls()
    for url in urls:
        status, monitors = Monitor.objects.check_url(url)
        logger.info("%s - %s monitor(s): %s", url, monitors.count(), status)
        if status == MonitorStatus.OFFLINE:
            send_mail_to_client.delay(url=url)
