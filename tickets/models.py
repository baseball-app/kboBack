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

class Response(models.Model):
    RESPONSE1 = "메롱"
    RESPONSE2 = "웃음"
    RESPONSE3 = "화남"
    RESPONSE4 = "욕설"
    RESPONSE5 = "불쾌"
    RESPONSE6 = "엄지척"
    RESPONSE7 = "위손가락"
    RESPONSE8 = "엄지아래"
    RESPONSE9 = "박수"
    RESPONSE_CHOICES = (
        (RESPONSE1, "매롱"),
        (RESPONSE2, "웃음"),
        (RESPONSE3, "화남"),
        (RESPONSE4, "욕설"),
        (RESPONSE5, "불쾌"),
        (RESPONSE6, "엄지척"),
        (RESPONSE7, "위손가락"),
        (RESPONSE8, "엄지아래"),
        (RESPONSE9, "박수"),
    )
    response = models.CharField(
        choices=RESPONSE_CHOICES, max_length=30, blank=True)
    ticket_id = models.ForeignKey('tickets.Ticket', on_delete=models.CASCADE)
    writer_id = models.ForeignKey('users.User', on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)