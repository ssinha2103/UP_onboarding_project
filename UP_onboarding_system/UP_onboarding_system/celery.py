from __future__ import absolute_import, unicode_literals
import os
# import settings
from celery import Celery
from celery.signals import setup_logging
from django_structlog.celery.steps import DjangoStructLogInitStep
from django.conf import settings
import logging

import structlog

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'UP_onboarding_system.settings')

app = Celery('UP_onboarding_system')


# A step to initialize django-structlog
# app.steps['worker'].add(DjangoStructLogInitStep)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

#
# @setup_logging.connect
# def config_loggers(*args, **kwargs):
#     from logging.config import dictConfig  # noqa
#     from django.conf import settings  # noqa
#
#     dictConfig(settings.LOGGING)


if __name__ == '__main__':
    app.start()
