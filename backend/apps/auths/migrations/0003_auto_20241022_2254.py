# Generated by Django 3.2.18 on 2024-10-22 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auths', '0002_socialinfo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialinfo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created_at'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='socialinfo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated_at'),
        ),
    ]