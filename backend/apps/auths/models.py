from django.db import models

from apps.auths.chocies import SocialTypeEnum
from base.models import TimeStampModel


class SocialInfo(TimeStampModel):
    user = models.ForeignKey("users.User", on_delete=models.DO_NOTHING)
    social_id = models.BigIntegerField()
    social_user = models.CharField(max_length=255)
    type = models.PositiveSmallIntegerField("type", choices=SocialTypeEnum.full_choices())
