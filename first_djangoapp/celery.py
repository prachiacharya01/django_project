from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import Settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_djangoapp.settings')
app = Celery('first_djangoapp')
app.conf.enable_utc = False
app.conf.update(timezone = 'Asia/Kolkata')
app.config_from_object('django.conf.settings', namespace='CELERY')

# CELERY BEAT
app.conf.beat_scheduler = {
    
}

app.autodiscover_tasks()

@app.task(bind=True)

def debug_task(self):
    print(f'("Result: ",{self.request!r})')