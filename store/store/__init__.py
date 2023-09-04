import os

import django

from .celery import app as celery_app

os.environ['DJANGO_SETTINGS_MODULE'] = 'store.settings'

__all__ = ('celery_app',)

django.setup()
