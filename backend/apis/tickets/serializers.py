from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.tickets.models import Ticket

class TicketSerializer(ModelSerializer):
    class Meta:
        fields = ['id', 'date', 'result', 'weather', 'is_ballpark', 'score_our', 'score_opponent', 'starting_pitchers',
                  'gip_place', 'image', 'food', 'memo', 'is_homeballpark', 'created_at', 'updated_at', 'ballpark',
                  'game', 'opponent', 'writer']