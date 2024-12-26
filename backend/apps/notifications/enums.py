from django.db import models


class NOTIFICATION_TYPE(models.TextChoices):
    TEST = "TEST", ("테스트")
    WELCOME = "WELCOME", ("환영 인사")
    NORMAL = "NORMAL", ("일반")
