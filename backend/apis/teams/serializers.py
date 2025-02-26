from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.teams.models import Team


class TeamsSerializer(ModelSerializer):
    id = serializers.IntegerField(required=True)
    name = serializers.CharField(read_only=True)
    logo_url = serializers.CharField(read_only=True)

    class Meta:
        model = Team
        fields = ["id", "name", "logo_url"]
