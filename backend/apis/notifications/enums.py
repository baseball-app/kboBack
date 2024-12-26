from django.db import models


class NOTIFICATION_READ_TYPE(models.TextChoices):
    ALL_NOTIFICATIONS = "ALL", ("전체 알림")
    FRIEND_FEEDBACK_NOTIFICATION = "FRIEND_FEEDBACK", ("친구의 반응 알림")
    FRIEND_UPDATE_NOTIFICATION = "NORMAL", ("친구의 새소식 알림")
