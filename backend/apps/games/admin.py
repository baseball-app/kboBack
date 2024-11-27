from django.contrib import admin
from . import models


@admin.register(models.Game)
class AdminGame(admin.ModelAdmin):
    pass


@admin.register(models.Ballpark)
class AdminBallpark(admin.ModelAdmin):
    pass
