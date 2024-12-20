# Generated by Django 5.1.2 on 2024-11-19 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ballpark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ballparks', to='teams.team')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('game_date', models.DateTimeField()),
                ('ballpark', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='games', to='games.ballpark')),
                ('team_away', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='away_games', to='teams.team')),
                ('team_home', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='home_games', to='teams.team')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
