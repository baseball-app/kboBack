# Generated by Django 5.1.2 on 2024-12-18 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('message', models.TextField()),
                ('type', models.CharField(choices=[('TEST', '테스트'), ('WELCOME', '환영 인사'), ('NORMAL', '일반')], default='NORMAL', max_length=15)),
                ('is_read', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
