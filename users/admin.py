from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.User)
class CustomUser(admin.ModelAdmin):
    pass

@admin.register(models.Friendship)
class Frientship(admin.ModelAdmin):
    pass
