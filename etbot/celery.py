from __future__ import absolute_import, unicode_literals
import os, environ, sys
from celery import Celery
from etbot.settings import BASE_DIR


env = environ.Env()
env.read_env(os.path.join(BASE_DIR, '.env'))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'etbot.settings')

app = Celery('etbot')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
