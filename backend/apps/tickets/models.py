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

    only_me = models.BooleanField(default=False)
    is_double = models.BooleanField(default=False)

    favorite = models.BooleanField(default=False)

    laugh = models.IntegerField(default=0,help_text="웃음 이모지")
    wink = models.IntegerField(default=0,help_text="윙크 이모지")
    good = models.IntegerField(default=0,help_text="따봉 이모지")
    clap = models.IntegerField(default=0, help_text="박수 이모지")
    point_up = models.IntegerField(default=0, help_text="검지 손가락 위 이모지")
    petulance = models.IntegerField(default=0, help_text="짜증 이모지")
    confused = models.IntegerField(default=0, help_text="혼란 이모지")
    dislike = models.IntegerField(default=0, help_text="싫은 이모지")
    rage = models.IntegerField(default=0, help_text="격노 이모지")
    victory = models.IntegerField(default=0, help_text="브이 이모지")

    hometeam_id = models.CharField(default=0)
    awayteam_id = models.CharField(default=0)

    direct_yn = models.BooleanField(default=False)
    is_cheer = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.date} - {self.result} ({self.writer})"