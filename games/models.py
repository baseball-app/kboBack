from django.db import models

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=30)
    logo =  models.ImageField(upload_to='images/')

class Ballpark(models.Model):
    name = models.CharField(max_length=50)
    team = models.ForeignKey('games.Team', related_name='ballparks', on_delete = models.SET_NULL, null=True, blank=False)

class Game(models.Model):
    date = models.DateField()
    team_home = models.ManyToManyField("games.Team", related_name ='home_games', blank=False)
    team_away = models.ManyToManyField("games.Team", related_name ='away_games', blank=False)
    ballpark = models.ManyToManyField("games.Ballpark", related_name="games", blank=False)
    time = models.TimeField()