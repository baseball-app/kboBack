# Generated by Django 3.2.18 on 2024-10-04 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_auto_20240924_1611'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='user_id',
            new_name='writer',
        ),
    ]
