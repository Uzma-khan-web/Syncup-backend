import os
from celery import celery
from django.conf import settings

# Django settings ko Celery ke liye set karein
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('syncup_api')

# Settings file se 'CELERY' prefix wali configuration read karein
app.config_from_object('django.conf:settings', namespace='CELERY')

# Har app ke andar 'tasks.py' file ko automatically dhundein
app.autodiscover_tasks()