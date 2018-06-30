from celery import shared_task
from django.core.management import call_command


@shared_task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@shared_task
def check_monitors():
    call_command('checkurls', mail_clients=True)
