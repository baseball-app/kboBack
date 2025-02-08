from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.tickets.models import Ticket

# 상세용 Serialize
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket  # 여기서 Ticket 모델을 지정합니다.
        fields = ['id', 'date', 'result', 'weather', 'is_ballpark', 'score_our', 'score_opponent', 'starting_pitchers',
                  'gip_place', 'image', 'food', 'memo', 'is_homeballpark', 'created_at', 'updated_at', 'ballpark',
                  'game', 'opponent', 'writer', 'like', 'love', 'haha', 'yay', 'wow', 'sad', 'angry','only_me', 'is_double']

# 리스트용 Serialize
class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "date", "writer_id", "game_id", "opponent_id","ballpark_id")

# 수정용 Serialize
class TicketUpdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket  # 여기서 Ticket 모델을 지정합니다.
        fields = ['id','date', 'result', 'weather', 'is_ballpark', 'score_our', 'score_opponent', 'starting_pitchers',
                  'gip_place', 'image', 'food', 'memo', 'is_homeballpark','updated_at', 'ballpark_id',
                  'game_id', 'opponent_id', 'writer_id', 'only_me']

# 반응용 Serialize
class TicketReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id','like','love','haha','yay','wow','sad','angry']

# 삭제용 Serialize
class TicketDelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id']