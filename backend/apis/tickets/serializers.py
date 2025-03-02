from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apis.tickets.service import TicketService
from apps.tickets.models import Ticket

from rest_framework import serializers
import logging

logger = logging.getLogger(__name__)

# 상세용 Serialize
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket  # 여기서 Ticket 모델을 지정합니다.
        fields = ['id', 'date', 'result', 'weather', 'is_ballpark', 'score_our', 'score_opponent', 'starting_pitchers',
                  'gip_place', 'image', 'food', 'memo', 'is_homeballpark', 'created_at', 'updated_at', 'ballpark',
                  'game', 'opponent', 'writer', 'like', 'love', 'haha', 'yay', 'wow', 'sad', 'angry','only_me', 'is_double', 'favorite']

# 리스트용 Serialize
class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'date', 'writer_id', 'game_id', 'opponent_id','ballpark_id','favorite']

# 등록용 Serialize
class TicketAddSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False)

    class Meta:
        model = Ticket
        fields = ['id', 'date', 'result', 'weather', 'is_ballpark', 'score_our', 'score_opponent', 'starting_pitchers',
                  'gip_place', 'image', 'food', 'memo', 'is_homeballpark', 'created_at', 'updated_at', 'ballpark',
                  'game', 'opponent', 'writer', 'only_me', 'is_double', 'favorite']

    def create(self, validated_data):
        user_id = validated_data.get('writer')
        image = validated_data.pop('image', None)
        ticket = Ticket.objects.create(**validated_data)
        if image:
            image_url = TicketService.upload_to_s3(image, user_id)
            ticket.image_url = image_url  # 모델에 image_url 필드가 있어야 합니다
            ticket.save()
        return ticket

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

class TicketFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id','favorite']