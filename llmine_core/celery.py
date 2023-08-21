import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "llmine_core.settings")
app = Celery("llmine_core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
