from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apis.tickets.serializers import TicketSerializer
from apis.tickets.serializers import TicketListSerializer
from apis.tickets.serializers import TicketUpdSerializer
from apis.tickets.serializers import TicketAddSerializer
from apis.tickets.serializers import TicketCalendarSerializer
from apis.tickets.serializers import TicketReactionSerializer

from apis.tickets.swagger import (
    SWAGGER_TICKETS_ADD,
    SWAGGER_TICKETS_UPD,
    SWAGGER_TICKETS_DEL,
    SWAGGER_TICKETS_LIST,
    SWAGGER_TICKETS_REACTION_VIEW,
    SWAGGER_TICKETS_REACTION,
    SWAGGER_TICKETS_DETAIL,
    SWAGGER_WIN_RATE_CALCULATION,
    SWAGGER_TICKETS_FAVORITE,
    SWAGGER_WEEKDAY_MOST_WIN,
    SWAGGER_BALLPARK_MOST_VIEW,
    SWAGGER_OPPONENT_MOST_WIN,
    SWAGGER_LONGEST_WINNING_STREAK,
    SWAGGER_WIN_PERCENT,
    SWAGGER_TICKETS_CALENDAR_LOG,
    SWAGGER_TICKETS_DIRECT_ADD,
)
from apps.notifications.enums import NOTIFICATION_TYPE
from apps.tickets.models import Ticket
from apps.games.models import Game
from apps.teams.models import UserTeam
from apps.users.models import Friendship

from .service import TicketService
from django.db.models import Count, Case, When, IntegerField, F, Q
from django.db.models import Window

from django.db.models.functions import Lag
from conf.celery import create_multiple_notifications

import logging
import datetime

logger = logging.getLogger(__name__)


@extend_schema_view(
    ticket_add=SWAGGER_TICKETS_ADD,
    ticket_upd=SWAGGER_TICKETS_UPD,
    ticket_del=SWAGGER_TICKETS_DEL,
    ticket_list=SWAGGER_TICKETS_LIST,
    ticket_reaction_view=SWAGGER_TICKETS_REACTION_VIEW,
    ticket_reaction=SWAGGER_TICKETS_REACTION,
    ticket_detail=SWAGGER_TICKETS_DETAIL,
    ticket_favorite=SWAGGER_TICKETS_FAVORITE,
    win_rate_calculation=SWAGGER_WIN_RATE_CALCULATION,
    weekday_most_win=SWAGGER_WEEKDAY_MOST_WIN,
    ballpark_most_view=SWAGGER_BALLPARK_MOST_VIEW,
    opponent_most_win=SWAGGER_OPPONENT_MOST_WIN,
    longest_winning_streak=SWAGGER_LONGEST_WINNING_STREAK,
    win_percnet=SWAGGER_WIN_PERCENT,
    ticket_calendar_log=SWAGGER_TICKETS_CALENDAR_LOG,
    ticket_direct_add=SWAGGER_TICKETS_DIRECT_ADD,
)
class TicketsViewSet(
    GenericViewSet,
):
    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])  # 직관 일기 리스트로 보기
    def ticket_list(self, request):
        try:
            user = request.user

            # 쿼리 파라미터 가져오기
            team_id = self.request.query_params.get("team_id")  # Team ID 입력값

            # team_id가 비어 있는 경우 처리
            if not team_id or team_id.strip() == "":
                team_id = None  # 빈값을 None으로 처리

            # 쿼리셋 초기화
            queryset = Ticket.objects.none()

            # 쿼리 파라미터 가져오기 및 변환
            favorite = self.request.query_params.get("favorite", "").lower()
            is_cheer = self.request.query_params.get("is_cheer", "").lower()

            # 문자열 값을 boolean 값으로 변환
            if favorite is not None:
                if favorite.lower() in ["true", "t", "1"]:
                    favorite = True
                elif favorite.lower() in ["false", "f", "0"]:
                    favorite = False
                else:
                    return Response({"detail": "favorite 값이 유효하지 않습니다."}, status=400)

            if is_cheer is not None:
                if is_cheer.lower() in ["true", "t", "1"]:
                    is_cheer = True
                elif is_cheer.lower() in ["false", "f", "0"]:
                    is_cheer = False
                else:
                    return Response({"detail": "is_cheer 값이 유효하지 않습니다."}, status=400)

            if team_id:
                logger.info("team_id ::", team_id)
                queryset = Ticket.objects.filter(
                    writer=user,  # 작성자 필터링
                    is_cheer=True,  # is_cheer 조건 강제
                    favorite=favorite,
                ).filter(
                    Q(ballpark__team__id=team_id)  # Ballpark와 연결된 Team ID 필터링
                    | Q(opponent__id=team_id)  # Opponent ID 필터링
                )
            else:
                # team_id가 없는 경우 기본 필터링 조건만 적용
                queryset = Ticket.objects.filter(writer=user, is_cheer=is_cheer, favorite=favorite)

            # 직렬화 및 응답 반환
            serializer = TicketListSerializer(queryset.distinct(), many=True)
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error occurred in ticket_list: {e}")
            return Response({"error": str(e)}, status=500)

    @action(methods=["GET"], detail=False, permission_classes=[AllowAny])  # 티켓 상세 보기
    def ticket_detail(self, request):
        user = request.user
        ticket_id = request.query_params.get("id")
        ticket_date = request.query_params.get("date")
        target_id = request.query_params.get("target_id")

        if ticket_id:
            try:
                tickets = Ticket.objects.filter(id=ticket_id, writer=target_id)  # 해당 ID의 티켓 객체 가져오기
                if not tickets.exists():
                    return Response({"detail": "티켓을 찾지 못하였습니다."}, status=status.HTTP_404_NOT_FOUND)
            except Ticket.DoesNotExist:
                return Response({"detail": "티켓을 찾지 못하였습니다."}, status=status.HTTP_404_NOT_FOUND)
        elif ticket_date:
            try:
                tickets = Ticket.objects.filter(date=ticket_date, writer=target_id)  # 해당 Date의 티켓 객체 가져오기
                if not tickets.exists():
                    return Response({"detail": "티켓을 찾지 못하였습니다."}, status=status.HTTP_404_NOT_FOUND)
            except Ticket.DoesNotExist:
                return Response({"detail": "티켓을 찾지 못하였습니다."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"detail": "티켓id값 또는 date값이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = TicketSerializer(tickets, many=True)  # 티켓 직렬화
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])  # 티켓 추가하기
    def ticket_add(self, request):
        user = request.user
        try:
            # game_id 가져오기
            game_id = request.data.get("game")

            # game_id가 None, 빈 문자열, 공백 문자열인 경우 기본값 처리
            if not game_id or str(game_id).strip() == "":
                game = 1
                ballpark_id = 1
                opponent_id = 1
            else:
                # game_id가 숫자인지 확인
                if not str(game_id).isdigit():
                    return Response({"error": "game_id must be a valid number"}, status=400)

                # game_id가 유효한 숫자인 경우 처리
                game_id = int(game_id)
                try:
                    game = Game.objects.get(id=game_id)
                    ballpark_id = game.ballpark.id
                    opponent_id = game.team_away.id
                except Game.DoesNotExist:
                    return Response({"error": "Invalid game ID"}, status=400)

            # 요청 데이터 복사 및 game_id 설정
            data = request.data.copy()
            data["game"] = game_id if game_id else 1  # 기본값 삽입

            # ticket 테이블에서 일치하는 date 값의 개수를 확인
            match_count = Ticket.objects.filter(date=data.get("date"), writer=user).count()

            # 하루에 2건까지 추가 가능
            if match_count >= 2:
                return Response({"error": "하루 티켓 발권 가능 갯수를 초과하였습니다."}, status=400)

            # Serializer를 사용해 데이터 유효성 검사 및 저장
            serializer = TicketAddSerializer(data=data, context={"request": request})
            if serializer.is_valid():
                ticket = serializer.save(writer=user, ballpark=ballpark_id, opponent=opponent_id)

                friend_ids = list(Friendship.objects.filter(source=user).values_list("target_id", flat=True))
                if friend_ids:
                    message = f"{user.nickname}님이 새로운 티켓을 등록했습니다."
                    create_multiple_notifications.delay(
                        me=user.id,
                        user_ids=friend_ids,
                        notification_type=NOTIFICATION_TYPE.FRIEND_UPDATE,
                        message=message,
                        ticket_id=ticket.id,
                    )
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)

        except Exception as e:
            logger.error(f"Error occurred in ticket_add: {e}")
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=500)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])  # 직관 일기 수정하기
    def ticket_upd(self, request):
        try:
            ticket_identifier = request.data.get("id")
            if not ticket_identifier:
                return Response({"detail": "티켓 id값이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                ticket = Ticket.objects.get(id=ticket_identifier)
            except Ticket.DoesNotExist:
                return Response({"detail": "티켓을 찾지 못하였습니다."}, status=status.HTTP_404_NOT_FOUND)

            # 입력 데이터 복사 후 image 필드 제거 조건 적용
            updated_data = request.data.copy()

            serializer = TicketUpdSerializer(ticket, data=updated_data, partial=True, context={"request": request})

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])  # 티켓 삭제
    def ticket_del(self, request):
        ticket_id = request.data.get("id")
        if not ticket_id:
            return Response({"error": "삭제하고자 하는 티켓 ID를 설정해주세요."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Ticket.DoesNotExist:
            return Response({"error": "해당 티켓을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])  # 티켓 반응 보기 (단건)
    def ticket_reaction_view(self, request):
        target_id = request.query_params.get("target_id")

        try:
            # 단건 조회
            ticket = Ticket.objects.get(id=target_id)
        except Ticket.DoesNotExist:
            return Response({"message": "티켓을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 단건 직렬화
        serializer = TicketReactionSerializer(ticket)  # many=False (default)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])  # 티켓에 반응 추가/삭제하기
    def ticket_reaction(self, request):
        user = request.user
        ticket_identifier = request.data.get("id")
        reaction_pos = request.data.get("reaction_pos")
        reaction_type = request.data.get("reaction_type")

        # ticket_identifier에 해당하는 티켓 객체 조회
        try:
            ticket = Ticket.objects.get(id=ticket_identifier)
        except Ticket.DoesNotExist:
            return Response({"message": "티켓을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

        # 티켓의 작성자가 현재 id일 경우 service 접근 금지
        if ticket.writer.id == user.id:
            return Response(
                {"message": "자신의 티켓에는 반응을 추가/삭제할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        service = TicketService()

        if reaction_pos == "add":  # 반응 추가
            service.add_reaction(ticket_identifier, reaction_type)
            message = "반응 추가 성공"

            notification_message = f"{user.nickname}님이 반응을 남겼습니다."
            create_multiple_notifications.delay(
                me=user.id,
                user_ids=[ticket.writer.id],
                notification_type=NOTIFICATION_TYPE.FRIEND_FEEDBACK,
                message=notification_message,
                ticket_id=ticket.id,
            )

        elif reaction_pos == "del":  # 반응 삭제
            service.del_reaction(ticket_identifier, reaction_type)
            message = "반응 삭제 성공"
        else:
            return Response({"message": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)

        response_data = {"message": message, "ticket_id": ticket_identifier, "reaction_pos": reaction_pos}

        return Response(response_data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])  # 최애경기 티켓 선정
    def ticket_favorite(self, request):
        try:
            ticket_id = request.data.get("id")
            favorite_status = request.data.get("favorite_status")
        except KeyError:
            return Response({"error": "요청 데이터에 'id'와 'set_favorite' 값이 필요합니다."}, status=400)

        service = TicketService()
        service.set_favorite(ticket_id, favorite_status)
        message = "적용 성공"

        response_data = {"message": message, "ticket_id": ticket_id, "favorite_status": favorite_status}

        return Response(response_data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])  # 경기 결과 통계 추산
    def win_rate_calculation(self, request):
        user = request.user
        team_id = UserTeam.objects.get(user_id=user).team_id  # myTeam id 뽑아오기

        # 티켓에서 마이팀 해당되는것만 조회하기(직관)
        queryset_is_ballpark = (
            Ticket.objects.filter(writer=user, is_ballpark=True)
            .filter(Q(opponent=team_id) | Q(ballpark__team=team_id) | Q(hometeam_id=team_id) | Q(awayteam_id=team_id))
            .aggregate(
                win_count=Count(Case(When(result="승리", then=1), output_field=IntegerField())),
                loss_count=Count(Case(When(result="패배", then=1), output_field=IntegerField())),
                draw_count=Count(Case(When(result="무승부", then=1), output_field=IntegerField())),
                cancel_count=Count(Case(When(result="취소", then=1), output_field=IntegerField())),
            )
        )

        # 티켓에서 마이팀 해당되는것만 조회하기(집관)
        queryset_is_not_ballpark = (
            Ticket.objects.filter(writer=user, is_ballpark=False)
            .filter(Q(opponent=team_id) | Q(ballpark__team=team_id) | Q(hometeam_id=team_id) | Q(awayteam_id=team_id))
            .aggregate(
                win_count=Count(Case(When(result="승리", then=1), output_field=IntegerField())),
                loss_count=Count(Case(When(result="패배", then=1), output_field=IntegerField())),
                draw_count=Count(Case(When(result="무승부", then=1), output_field=IntegerField())),
                cancel_count=Count(Case(When(result="취소", then=1), output_field=IntegerField())),
            )
        )

        result = {"is_ballpark_win_rate": queryset_is_ballpark, "is_not_ballpark_win_rate": queryset_is_not_ballpark}

        return Response(result, status=200)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])  # 가장 승리 많이 한 요일 산출
    def weekday_most_win(self, request):
        user = request.user
        team_id = UserTeam.objects.get(user_id=user).team_id  # myTeam id 뽑아오기

        # 티켓에서 마이팀 해당되는것만 조회하기
        queryset = Ticket.objects.filter(writer=user, result="승리", is_cheer=True).filter(
            Q(opponent=team_id) | Q(ballpark__team=team_id) | Q(hometeam_id=team_id) | Q(awayteam_id=team_id)
        )

        service = TicketService()
        most_wins_day = service.calculate_weekday_wins(queryset)

        return Response({"most_wins_day": most_wins_day})

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])  # 가장 많이 관람한 구장 산출
    def ballpark_most_view(self, request):
        user = request.user
        # team_id = UserTeam.objects.get(user_id=user).team_id  # myTeam id 뽑아오기

        queryset = Ticket.objects.filter(writer=user, is_ballpark=True)
        service = TicketService()
        most_wins_ballpark = service.calculate_most_win_ballpark(queryset)

        return Response({"most_wins_ballpark": most_wins_ballpark})

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])  # 가장 상대로 승리 많이한 구단 산출
    def opponent_most_win(self, request):
        user = request.user
        team_id = UserTeam.objects.get(user_id=user).team_id  # myTeam id 뽑아오기

        queryset = Ticket.objects.filter(writer=user, result="승리", is_cheer=True).filter(
            Q(opponent=team_id) | Q(ballpark__team=team_id) | Q(hometeam_id=team_id) | Q(awayteam_id=team_id)
        )

        service = TicketService()
        most_wins_opponent = service.calculate_most_win_opponent(queryset)

        return Response({"most_wins_opponent": most_wins_opponent})

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])  # 가장 긴 연승 기간 찾기
    def longest_winning_streak(self, request):
        user = request.user
        team_id = UserTeam.objects.get(user_id=user).team_id  # myTeam id 뽑아오기

        # 티켓 승리 내역 가져오기
        queryset = (
            Ticket.objects.filter(writer=user, result="승리", is_cheer=True)
            .filter(Q(opponent=team_id) | Q(ballpark__team=team_id) | Q(hometeam_id=team_id) | Q(awayteam_id=team_id))
            .annotate(prev_date=Window(expression=Lag("date", 1), partition_by=[F("writer")], order_by=F("date").asc()))
            .order_by("date")
        )
        # 가장 긴 연승 기간 계산
        max_streak = 0
        current_streak = 0
        prev_date = None

        for ticket in queryset:
            if prev_date and ticket.date == prev_date + datetime.timedelta(days=1):
                current_streak += 1
            else:
                current_streak = 1
            if current_streak > max_streak:
                max_streak = current_streak
            prev_date = ticket.date

        return Response({"longest_winning_streak": max_streak})

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])  # 집관 & 직관 경기 승률 퍼센티지 추산
    def win_percnet(self, request):
        user = request.user
        team_id = UserTeam.objects.get(user_id=user).team_id  # myTeam id 뽑아오기

        # 쿼리 파라미터에서 is_ballpark 값 가져오기
        is_ballpark = request.query_params.get("is_ballpark")

        # 문자열 값을 boolean 값으로 변환
        if is_ballpark is not None:
            if is_ballpark.lower() in ["true", "t", "1"]:
                is_ballpark = True
            elif is_ballpark.lower() in ["false", "f", "0"]:
                is_ballpark = False
            else:
                return Response({"detail": "is_ballpark 값이 유효하지 않습니다."}, status=400)

        queryset = Ticket.objects.filter(writer=user, is_ballpark=is_ballpark, is_cheer=True).filter(
            Q(opponent=team_id) | Q(ballpark__team=team_id) | Q(hometeam_id=team_id) | Q(awayteam_id=team_id)
        )

        total_games = queryset.count()
        wins = queryset.filter(result="승리").count()

        if total_games == 0:
            win_percent = 0
        else:
            win_percent = int((wins / total_games) * 100)

        return Response({"win_percent": win_percent}, status=200)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def ticket_calendar_log(self, request):
        user_id = request.GET.get("user_id")
        input_date = request.GET.get("date")  # 'YYYY-MM' 형식의 날짜 입력 받기

        filters = {}

        if user_id:
            filters["writer"] = user_id

        if input_date:
            input_year, input_month = map(int, input_date.split("-"))
            filters["date__year"] = input_year
            filters["date__month"] = input_month

        tickets = Ticket.objects.filter(**filters)
        serializer = TicketCalendarSerializer(tickets, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
