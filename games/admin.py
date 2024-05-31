from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Game)
class Game(admin.ModelAdmin):
    pass

@admin.register(models.Team)
class Team(admin.ModelAdmin):
    pass

@admin.register(models.Ballpark)
class Ballpark(admin.ModelAdmin):
    pass
