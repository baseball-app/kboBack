from django.contrib import admin
from . import models


@admin.register(models.Ticket)
class Ticket(admin.ModelAdmin):
    pass
