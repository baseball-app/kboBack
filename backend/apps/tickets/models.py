from django.db import models


class Ticket(models.Model):
    RESULT1 = "승리"
    RESULT2 = "패배"
    RESULT3 = "무승부"
    RESULT4 = "취소"
    RESULT_CHOICES = (
        (RESULT1, "승리"),
        (RESULT2, "패배"),
        (RESULT3, "무승부"),
        (RESULT4, "취소"),
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

    writer = models.ForeignKey("users.User", on_delete=models.CASCADE)
    date = models.DateField()
    game = models.ForeignKey("games.Game", on_delete=models.CASCADE, default=1, related_name="ticket_game")
    result = models.CharField(choices=RESULT_CHOICES, max_length=10)
    weather = models.CharField(choices=WEATHER_CHOICES, max_length=30)
    is_ballpark = models.BooleanField(default=True)
    score_our = models.IntegerField(default=0)
    score_opponent = models.IntegerField(default=0)
    opponent = models.ForeignKey(
        "teams.Team",
        on_delete=models.SET_NULL,
        null=True,
        related_name="ticket_team_away"
    )
    starting_pitchers = models.CharField(max_length=255)
    ballpark = models.ForeignKey("games.Ballpark", on_delete=models.SET_NULL, null=True, related_name="ticket_ballpark")
    gip_place = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    food = models.CharField(max_length=255, null=True, blank=True)
    memo = models.TextField(null=True, blank=True)
    is_homeballpark = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    like = models.IntegerField(default=0)
    love = models.IntegerField(default=0)
    haha = models.IntegerField(default=0)
    yay = models.IntegerField(default=0)
    wow = models.IntegerField(default=0)
    sad = models.IntegerField(default=0)
    angry = models.IntegerField(default=0)

    only_me = models.BooleanField(default=False)
    is_double = models.BooleanField(default=False)

    favorite = models.BooleanField(default=False)

    direct_home_team = models.CharField(max_length=30, default="")
    direct_away_team = models.CharField(max_length=30, default="")

    direct_yn = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} - {self.result} ({self.writer})"