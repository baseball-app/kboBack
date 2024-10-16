from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=30)
    logo = models.ImageField(upload_to='images/')


class Ballpark(models.Model):
    name = models.CharField(max_length=50)
    team = models.ForeignKey('games.Team', related_name='ballparks', on_delete=models.SET_NULL, null=True, blank=False)


class Game(models.Model):
    date = models.DateField()
    team_home = models.ForeignKey('games.Team', on_delete=models.CASCADE, related_name='home_games')
    team_away = models.ForeignKey('games.Team', on_delete=models.CASCADE, related_name='away_games')
    ballpark = models.ForeignKey('games.Ballpark', on_delete=models.CASCADE, related_name="games")
    time = models.TimeField()
