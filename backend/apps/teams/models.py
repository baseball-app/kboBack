from django.db import models

from base.models import TimeStampModel


class Team(models.Model):
    name = models.CharField(max_length=30)
    logo_url = models.CharField(max_length=255)


class UserTeam(TimeStampModel):
    user = models.ForeignKey("users.User", related_name="user", on_delete=models.DO_NOTHING)
    team = models.ForeignKey("teams.Team", related_name="team", on_delete=models.DO_NOTHING)
