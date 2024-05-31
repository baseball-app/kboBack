
from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Ticket)
class Ticket(admin.ModelAdmin):
    pass
