# Generated by Django 5.1.2 on 2025-04-03 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0012_remove_ticket_angry_remove_ticket_haha_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="victory",
            field=models.IntegerField(default=0, help_text="브이 이모지"),
        ),
    ]
