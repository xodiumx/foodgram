from __future__ import absolute_import
import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodgram.settings')

app = Celery('foodgram')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'delete-expired-tokens': {
        'task': 'users.tasks.delete_expired_tokens',
        'schedule': crontab(minute=0, hour=0),
    },
}
app.conf.timezone = 'UTC'
