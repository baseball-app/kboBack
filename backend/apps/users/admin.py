from django.contrib import admin
from . import models


@admin.register(models.User)
class User(admin.ModelAdmin):
    pass


@admin.register(models.Friendship)
class Friendship(admin.ModelAdmin):
    pass
