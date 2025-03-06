from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apis.tickets.service import TicketService
from apps.tickets.models import Ticket
from apps.games.models import Ballpark
from apps.teams.models import Team


from rest_framework import serializers
import logging

logger = logging.getLogger(__name__)

# 참조용 Serialize
class BallparkSerializer(serializers.ModelSerializer):
    team_id = serializers.PrimaryKeyRelatedField(source='team.id', read_only=True)

    class Meta:
        model = Ballpark
        fields = ['id', 'name', 'team_id']


class OpponentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ['id', 'name']

# 상세용 Serialize
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket  # 여기서 Ticket 모델을 지정합니다.
        fields = ['id', 'date', 'result', 'weather', 'is_ballpark', 'score_our', 'score_opponent', 'starting_pitchers',
                  'gip_place', 'image', 'food', 'memo', 'is_homeballpark', 'created_at', 'updated_at', 'ballpark',
                  'game', 'opponent', 'writer', 'like', 'love', 'haha', 'yay', 'wow', 'sad', 'angry','only_me', 'is_double', 'favorite', 'direct_home_team', 'direct_away_team', 'direct_yn', 'is_cheer_home']

# 리스트용 Serialize

class TicketListSerializer(serializers.ModelSerializer):
    ballpark = BallparkSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'date', 'writer_id', 'game_id', 'opponent_id', 'ballpark', 'is_double', 'favorite', 'direct_home_team', 'direct_away_team', 'direct_yn', 'is_cheer_home']

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
                  'gip_place', 'image', 'food', 'memo', 'is_homeballpark','updated_at', 'writer_id', 'only_me', 'direct_home_team', 'direct_away_team', 'is_cheer_home']

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

# 최애경기 선정용 Serialize
class TicketFavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id','favorite']

# 월 별 직관일기 목록용 Serialize
class TicketCalendarSerializer(serializers.ModelSerializer):
    ballpark = BallparkSerializer(read_only=True)
    opponent = OpponentSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id','date', 'result', 'writer_id','game_id','opponent','ballpark']


# 직접 등록용 Serialize
class TicketDirectAddSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False)
    writer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'date', 'result', 'weather', 'is_ballpark', 'score_our', 'score_opponent', 'starting_pitchers',
                  'gip_place', 'image', 'food', 'memo', 'is_homeballpark', 'created_at', 'updated_at', 'ballpark',
                  'game', 'opponent', 'writer', 'only_me', 'is_double', 'favorite', 'direct_home_team', 'direct_away_team', 'is_cheer_home']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        image = validated_data.pop('image', None)

        try:

            ticket = Ticket.objects.create(
                writer_id=user.id,
                ballpark_id=1, # ballpark와 opponent값은 임의로 1 설정 (관계키)
                opponent_id=1,
                direct_yn=True,
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



