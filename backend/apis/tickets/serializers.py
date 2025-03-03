from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apis.tickets.service import TicketService
from apps.tickets.models import Ticket
from apps.games.models import Ballpark


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
class BallparkSerializer(serializers.ModelSerializer):
    team_id = serializers.PrimaryKeyRelatedField(source='team.id', read_only=True)

    class Meta:
        model = Ballpark
        fields = ['id', 'name', 'team_id']

class TicketListSerializer(serializers.ModelSerializer):
    ballpark = BallparkSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'date', 'writer_id', 'game_id', 'opponent_id', 'ballpark', 'favorite']

# 등록용 Serializer
class TicketAddSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False)
    writer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'date', 'result', 'weather', 'is_ballpark', 'score_our', 'score_opponent', 'starting_pitchers',
                  'gip_place', 'image', 'food', 'memo', 'is_homeballpark', 'created_at', 'updated_at', 'ballpark',
                  'game', 'opponent', 'writer', 'only_me', 'is_double', 'favorite']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        image = validated_data.pop('image', None)
        game_id = validated_data.pop('game', None)

        ballpark_id = validated_data.pop('ballpark', None)
        opponent_id = validated_data.pop('opponent', None)

        try:
            ticket = Ticket.objects.create(
                writer_id=user.id,
                game=game_id,
                ballpark_id=ballpark_id,
                opponent_id=opponent_id,
                **validated_data
            )

            if image:
                image_url = TicketService.upload_to_s3(image, user.id)
                ticket.image = image_url
                ticket.save()
            return ticket

        except Exception as e:
            logger.error(f"Error occurred in TicketAddSerializer: {e}")
            raise serializers.ValidationError(f"An error occurred while creating the ticket: {e}")

# 수정용 Serialize
class TicketUpdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket  # 여기서 Ticket 모델을 지정합니다.
        fields = ['id','date', 'result', 'weather', 'is_ballpark', 'score_our', 'score_opponent', 'starting_pitchers',
                  'gip_place', 'image', 'food', 'memo', 'is_homeballpark','updated_at', 'writer_id', 'only_me']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        image = validated_data.pop('image', None)

        try:
            ticket = Ticket.objects.create(**validated_data)

            if image:
                image_url = TicketService.upload_to_s3(image, user.id)
                ticket.image = image_url
                ticket.save()
            return ticket

        except Exception as e:
            logger.error(f"Error occurred in TicketUpdSerializer: {e}")
            raise serializers.ValidationError(f"An error occurred while creating the ticket: {e}")

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