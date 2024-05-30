from django.db import models

# Create your models here.
class Ticket(models.Model):
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE)
    is_ballpark = models.IntegerField()
    ballpark = models.CharField(max_length=255)
    place = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    starting_pitchers = models.CharField(max_length=255)
    food = models.CharField(max_length=255)
    memo = models.TextField()
    is_home = models.IntegerField()
    date = models.DateTimeField()
