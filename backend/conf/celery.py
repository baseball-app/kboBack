import os
from celery import Celery, shared_task
from django.db import transaction

from conf.utils import set_environment

set_environment()

import django

django.setup()

from apps.tickets.models import Ticket
from apps.notifications.models import Notification
from apps.users.models import User

app = Celery("conf")

app.config_from_object(os.getenv("DJANGO_SETTINGS_MODULE"), namespace="CELERY")
app.autodiscover_tasks()


@shared_task(bind=True)
def create_multiple_notifications(self, me, user_ids, notification_type, message, ticket_id):
    try:
        with transaction.atomic():
            ticket = Ticket.objects.get(pk=ticket_id)
            me = User.objects.get(pk=me)
            notifications = [
                Notification(feedback_user=me, user_id=user_id, type=notification_type, message=message, ticket=ticket)
                for user_id in user_ids
            ]
            Notification.objects.bulk_create(notifications)
    except Exception as e:
        print(f"create_multiple_notifications errors: {e}")
