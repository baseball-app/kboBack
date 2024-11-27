from django.db import models

from base.models import TimeStampModel


class Ballpark(models.Model):
    name = models.CharField(max_length=50)
    team = models.ForeignKey("teams.Team", related_name="ballparks", on_delete=models.DO_NOTHING, null=True)


class Game(TimeStampModel):
    team_home = models.ForeignKey("teams.Team", on_delete=models.DO_NOTHING, related_name="home_games")
    team_away = models.ForeignKey("teams.Team", on_delete=models.DO_NOTHING, related_name="away_games")
    ballpark = models.ForeignKey("games.Ballpark", on_delete=models.DO_NOTHING, related_name="games")
    game_date = models.DateTimeField()
