from django.db import models

from apps.notifications.enums import NOTIFICATION_TYPE
from base.models import TimeStampModel


class Notification(TimeStampModel):
    feedback_user = models.ForeignKey(
        "users.User", related_name="notifications_feedback", on_delete=models.SET_NULL, null=True
    )
    user = models.ForeignKey("users.User", related_name="notifications", on_delete=models.CASCADE)
    ticket = models.ForeignKey("tickets.Ticket", related_name="notifications", on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    type = models.CharField(max_length=15, choices=NOTIFICATION_TYPE.choices, default=NOTIFICATION_TYPE.FRIEND_FEEDBACK)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.nickname}"

    class Meta:
        ordering = ["-created_at"]
