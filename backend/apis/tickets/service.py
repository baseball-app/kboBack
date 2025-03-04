from django.db.migrations.exceptions import NodeNotFoundError

from apps.tickets.models import Ticket
from apps.games.models import Ballpark
from apps.teams.models import Team
from django.db.models.functions import ExtractWeekDay
from django.db.models import Count

import logging
import base64
import uuid
from datetime import datetime
from io import BytesIO
import boto3
from PIL import Image
from django.conf import settings

logger = logging.getLogger(__name__)

class TicketService:
    def add_reaction(self, ticket_id,reaction_type):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            if reaction_type == "like":
                ticket.like += 1
            elif reaction_type == "love":
                ticket.love += 1
            elif reaction_type == "haha":
                ticket.haha += 1
            elif reaction_type == "yay":
                ticket.yay += 1
            elif reaction_type == "wow":
                ticket.wow += 1
            elif reaction_type == "sad":
                ticket.sad += 1
            elif reaction_type == "angry":
                ticket.angry += 1
            ticket.save()
        except Ticket.DoesNotExist:
            raise ValueError("티켓을 찾을 수 없습니다.")

    def del_reaction(self, ticket_id,reaction_type):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            if reaction_type == "like":
                ticket.like -= 1
            elif reaction_type == "love":
                ticket.love -= 1
            elif reaction_type == "haha":
                ticket.haha -= 1
            elif reaction_type == "yay":
                ticket.yay -= 1
            elif reaction_type == "wow":
                ticket.wow -= 1
            elif reaction_type == "sad":
                ticket.sad -= 1
            elif reaction_type == "angry":
                ticket.angry -= 1
            ticket.save()
        except Ticket.DoesNotExist:
            raise ValueError("티켓을 찾을 수 없습니다.")

    def set_favorite(self, ticket_id,favorite_status):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            if favorite_status == "excute":
                ticket.favorite = True
            elif favorite_status == "clear":
                ticket.favorite = False
            ticket.save()
        except Ticket.DoesNotExist:
            raise ValueError("티켓을 찾을 수 없습니다.")

    def calculate_weekday_wins(self, queryset):
        week_win_count = (
            queryset
            .annotate(weekday=ExtractWeekDay('game__game_date'))
            .values('weekday')
            .annotate(win_count=Count('weekday'))
            .order_by('-win_count')
            .first()
        )
        return week_win_count['weekday'] if week_win_count else None

    def calculate_most_win_ballpark(self, queryset):
        ballpark_win_count = (
            queryset
            .values('game__ballpark')
            .annotate(win_count=Count('game__ballpark'))
            .order_by('-win_count')
            .first()
        )

        if ballpark_win_count:
            ballpark_id = ballpark_win_count['game__ballpark']
            try:
                # `ballpark_id`의 이름을 조회
                ballpark_name = Ballpark.objects.get(id=ballpark_id).name
                return ballpark_name
            except Ballpark.DoesNotExist:
                return None

        return None

    def calculate_most_win_opponent(self, queryset):
        opponent_win_count = (
            queryset
            .values('game__team_away_id')
            .annotate(win_count=Count('game__team_away_id'))
            .order_by('-win_count')
            .first()
        )

        if opponent_win_count:
            opponent_id = opponent_win_count['game__team_away_id']
            try:
                # 'opponent_id'의 팀 명을 조회
                opponent_name = Team.objects.get(id=opponent_id).name
                return opponent_name
            except Team.DoesNotExist:
                return None

    @staticmethod
    def upload_to_s3(image, user_id):
        logger.info(f"user_id: {user_id}")
        current_date = datetime.now().strftime("%Y%m%d")
        unique_id = base64.urlsafe_b64encode(uuid.uuid4().bytes).decode("utf-8").rstrip("=")
        file_key = f"{user_id}/{current_date}_{unique_id}"

        s3 = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_S3_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_S3_SECRET_KEY,
        )

        img = Image.open(image)

        if img.mode != "RGB":
            img = img.convert("RGB")

        image_byte_array = BytesIO()
        img_resized = img.resize((110, 110))
        img_resized.save(image_byte_array, format="JPEG", quality=50, optimize=True)
        image_byte_array.seek(0)

        s3.upload_fileobj(
            image_byte_array,
            settings.AWS_S3_STORAGE_BUCKET_NAME,
            file_key,
            ExtraArgs={"ContentType": image.content_type},
        )

        return f"{settings.AWS_S3_CUSTOM_DOMAIN}{file_key}"


