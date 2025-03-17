from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apis.tickets.service import TicketService
from apps.tickets.models import Ticket
from apps.games.models import Ballpark
from apps.teams.models import Team
from urllib.parse import urlparse, unquote

from rest_framework import serializers
import logging
import re

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
    image = serializers.SerializerMethodField()  # 커스텀 필드 처리

    class Meta:
        model = Ticket
        fields = ['id', 'date', 'result', 'weather', 'is_ballpark', 'score_our', 'score_opponent', 'starting_pitchers',
                  'gip_place', 'image', 'food', 'memo', 'is_homeballpark', 'created_at', 'updated_at', 'ballpark',
                  'game', 'opponent', 'writer', 'laugh', 'wink', 'good', 'clap', 'point_up', 'petulance', 'confused',
                  'dislike', 'rage', 'only_me', 'is_double', 'favorite', 'hometeam_id', 'awayteam_id', 'direct_yn',
                  'is_cheer']

    def get_image(self, obj):
        # Logger로 이미지 데이터 출력
        logger.info(f"Raw image field: {obj.image}")

        if not obj.image:
            # 필드가 비어 있거나 None인 경우 처리
            return None

        # ImageFieldFile 객체에서 URL 가져오기
        if hasattr(obj.image, 'url'):
            raw_url = obj.image.url
        else:
            # .url 속성이 없으면 Invalid 반환
            return "Invalid image field"

        # URL 디코딩 및 슬래시 정리
        decoded_url = unquote(raw_url)

        # 앞에 붙은 불필요한 슬래시 제거
        if decoded_url.startswith('/'):
            decoded_url = decoded_url.lstrip('/')  # 모든 앞 슬래시 제거

        # http:// 또는 https:// 중복 슬래시를 정리
        cleaned_url = re.sub(r'^(https?:/)(/)+', r'\1/', decoded_url)

        # URL 형식 확인
        parsed = urlparse(cleaned_url)
        if parsed.scheme in ['http', 'https']:
            return cleaned_url  # S3 URL 또는 외부 URL 반환
        else:
            # 스킴 없는 로컬 경로 처리
            return f"Invalid or unsupported image path: {cleaned_url}"

# 리스트용 Serialize
class TicketListSerializer(serializers.ModelSerializer):
    ballpark = BallparkSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'date', 'writer_id', 'game_id', 'opponent_id', 'ballpark', 'is_double', 'favorite', 'hometeam_id', 'awayteam_id', 'direct_yn', 'is_cheer']

# 등록용 Serializer
class TicketAddSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False)
    writer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'date', 'result', 'weather', 'is_ballpark', 'score_our', 'score_opponent', 'starting_pitchers',
                  'gip_place', 'image', 'food', 'memo', 'is_homeballpark', 'created_at', 'updated_at', 'ballpark',
                  'game', 'opponent', 'writer', 'only_me', 'is_double', 'favorite', 'hometeam_id', 'awayteam_id', 'direct_yn', 'is_cheer']

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
                  'gip_place', 'image', 'food', 'memo', 'is_homeballpark','updated_at', 'writer_id', 'only_me', 'hometeam_id', 'awayteam_id', 'is_cheer']

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
        fields = ['id','laugh','wink','good','clap','point_up','petulance','confused','dislike','rage']

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
                  'game', 'opponent', 'writer', 'only_me', 'is_double', 'favorite', 'hometeam_id', 'awayteam_id', 'is_cheer']

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



