import os
from celery import Celery, shared_task
from django.db import transaction


from conf.utils import set_environment

set_environment()

import django

django.setup()

from apps.notifications.models import Notification

app = Celery("conf")

app.config_from_object(os.getenv("DJANGO_SETTINGS_MODULE"), namespace="CELERY")
app.autodiscover_tasks()


@shared_task(bind=True)
def create_user_notification(self, user_id, notification_type):
    try:
        with transaction.atomic():
            Notification.objects.create(user=user_id, notification_type=notification_type)

    except Exception as e:
        print(f"create_user_notification errors: {e}")
