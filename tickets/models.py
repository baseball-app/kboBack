from django.db import models

# Create your models here.
class Ticket(models.Model):
    RESULT1 = "승리"
    RESULT2="패배"
    RESULT3="무승부"
    RESULT4="취소"
    RESULT_CHOICES = (
        {RESULT1, "승리"},
        {RESULT2, "패배"},
        {RESULT3, "무승부"},
        {RESULT4, "취소"},
    )
    WEATHER1 = "맑음"
    WEATHER2 = "흐림"
    WEATHER3 = "비"
    WEATHER4 = "바람"
    WEATHER_CHOICES = (
        (WEATHER1, "맑음"),
        (WEATHER2, "흐림"),
        (WEATHER3, "비"),
        (WEATHER4, "바람"),
    )


    writer = models.ForeignKey('users.User', on_delete=models.CASCADE)
    date = models.DateField()
    game = models.ForeignKey('games.Game',on_delete=models.CASCADE, default=1)
    result = models.IntegerField(default=0)
    weather = models.IntegerField(default=0)
    is_ballpark = models.BooleanField(default=True)
    score_our = models.IntegerField(default=0)
    score_opponent = models.IntegerField(default=0)
    opponent = models.ForeignKey('games.Team', on_delete=models.SET_NULL, null=True)
    starting_pitchers = models.CharField(max_length=255)
    ballpark = models.ForeignKey('games.Ballpark',on_delete=models.SET_NULL, null=True)
    gip_place = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    food = models.CharField(max_length=255)
    memo = models.TextField()
    is_homeballpark = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 