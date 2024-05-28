import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TestAPI_core.settings')

app = Celery('TestAPI', broker='redis://127.0.0.1:6379/1')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
