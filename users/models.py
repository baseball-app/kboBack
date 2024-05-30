from django.db import models

# Create your models here.
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    nickname = models.CharField(max_length=255)
    favorite_team = models.IntegerField()
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='profile_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 모델 관리자
    def __str__(self):
        return self.username

class Friendship(models.Model):
    user1 = models.ForeignKey('User', related_name='friendships_initiated', on_delete=models.CASCADE)
    user2 = models.ForeignKey('User', related_name='friendships_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)