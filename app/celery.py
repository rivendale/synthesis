import os

from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
if not os.getenv('DJANGO_SETTINGS_MODULE', ''):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings.production')
CELERY_TASKS = [
    "app.api.helpers.validate_address",
]


app = Celery('app', include=CELERY_TASKS)


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.conf.beat_schedule = {
    'update bayc address nfts': {
        'task': 'update bayc address nfts',
        'schedule': crontab(minute=0, hour=0)
    },
}

app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
