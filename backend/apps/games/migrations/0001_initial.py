# Generated by Django 3.2.18 on 2024-10-22 11:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ballpark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('logo', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('ballpark', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='games.ballpark')),
                ('team_away', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_games', to='games.team')),
                ('team_home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='home_games', to='games.team')),
            ],
        ),
        migrations.AddField(
            model_name='ballpark',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ballparks', to='games.team'),
        ),
    ]
