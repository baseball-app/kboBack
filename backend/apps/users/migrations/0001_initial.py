# Generated by Django 4.2.13 on 2024-05-30 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('nickname', models.CharField(max_length=255)),
                ('favorite_team', models.IntegerField()),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('password', models.CharField(max_length=255)),
                ('profile_image', models.ImageField(upload_to='profile_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Friendship',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendships_initiated', to='users.user')),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friendships_received', to='users.user')),
            ],
        ),
    ]