import os
from celery import Celery

from conf.utils import set_environment

set_environment()

app = Celery("conf")

app.config_from_object(os.getenv("DJANGO_SETTINGS_MODULE"), namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
