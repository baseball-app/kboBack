from django.db import models


class NOTIFICATION_TYPE(models.TextChoices):
    TEST = "TEST", ("테스트")
    FRIEND_FEEDBACK = "FRIEND_FEEDBACK", ("친구의 반응 알림")
    FRIEND_UPDATE = "FRIEND_UPDATE", ("친구의 새소식 알림")
