from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from apps.games.models import Team
from apps.users.chocies import SocialTypeEnum


class UserManager(BaseUserManager):
    def create_user(self, nickname, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(nickname=nickname, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(nickname, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(max_length=255)
    social_info = models.ForeignKey('SocialInfo', null=True)
    my_team = models.ForeignKey('Team', on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField(max_length=255, unique=True)
    profile_image = models.ImageField(upload_to='profile_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.nickname


class SocialInfo(models.Model):
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    social_user = models.CharField(max_length=255)
    type = models.PositiveSmallIntegerField('type', choices=SocialTypeEnum.full_choices())


class Friendship(models.Model):
    user1 = models.ForeignKey('User', related_name='friendships_initiated', on_delete=models.CASCADE)
    user2 = models.ForeignKey('User', related_name='friendships_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1} and {self.user2} are friends"
