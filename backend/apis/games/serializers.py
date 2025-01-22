from rest_framework import serializers

from apis.teams.serializers import TeamsSerializer
from apps.games.models import Ballpark, Game


class BallparkSerializer(serializers.ModelSerializer):
    team_info = TeamsSerializer(source="team", read_only=True)

    class Meta:
        model = Ballpark
        fields = ["id", "name", "team_info"]


class GameSerializer(serializers.ModelSerializer):
    team_home_info = TeamsSerializer(source="team_home", read_only=True)
    team_away_info = TeamsSerializer(source="team_away", read_only=True)
    ballpark_info = BallparkSerializer(source="ballpark", read_only=True)

    class Meta:
        model = Game
        fields = ["id", "team_home_info", "team_away_info", "ballpark_info", "game_date"]
