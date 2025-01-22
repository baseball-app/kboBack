from rest_framework import serializers

from apps.games.models import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["id", "team_home", "team_away", "ballpark", "game_date"]
