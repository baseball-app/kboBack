from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models

from base.models import TimeStampModel


class UserManager(BaseUserManager):
    def create_user(self, nickname, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(nickname=nickname, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nickname, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(nickname, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampModel):
    nickname = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    profile_type = models.IntegerField(default=0)
    profile_image = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname"]

    def __str__(self):
        return self.nickname


class Friendship(TimeStampModel):
    source = models.ForeignKey("User", related_name="friendships_source", on_delete=models.DO_NOTHING)
    target = models.ForeignKey("User", related_name="friendships_target", on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ("source", "target")

    def str(self):
        return f"{self.source} and {self.target} are friends"