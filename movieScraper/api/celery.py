import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movieScraper.settings')

app = Celery('api',
             broker='amqp://broker-rabbitmq',
             backend='redis://broker-redis:6379/0')
# TODO : IMPORTANTE
# Mongo no es la herramienta para ocuparse como backend ya que al momento
# de querer leer los mensajes en otra aplicacion no lograba obetenerlos. Sin
# embaro con redis fue muy sencillo
# backend='mongodb://root:example@data-movies:27017/')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# The uppercase name-space means that all Celery configuration options
# must be specified in uppercase instead of lowercase,
# and start with CELERY_, so for example the task_always_eager
# setting becomes CELERY_TASK_ALWAYS_EAGER, and the broker_url
# setting becomes CELERY_BROKER_URL.
# This also applies to the workers settings, for intances,
# the worker_concurrency setting becomes CELERY_WORKER_CONCURRENCY.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
