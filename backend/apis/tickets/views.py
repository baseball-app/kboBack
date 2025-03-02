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

from apis.tickets.swagger import (SWAGGER_TICKETS_ADD, SWAGGER_TICKETS_UPD, SWAGGER_TICKETS_DEL, SWAGGER_TICKETS_LIST,
                                  SWAGGER_TICKETS_REACTION, SWAGGER_TICKETS_DETAIL, SWAGGER_WIN_RATE_CALCULATION, SWAGGER_TICKETS_FAVORITE,
                                  SWAGGER_WEEKDAY_MOST_WIN, SWAGGER_BALLPARK_MOST_WIN, SWAGGER_OPPONENT_MOST_WIN, SWAGGER_LONGEST_WINNING_STREAK,
                                  SWAGGER_WIN_SITE_PERCENT, SWAGGER_WIN_HOME_PERCENT)
from apps.tickets.models import Ticket
from apps.games.models import Game

from .service import TicketService
from django.db.models import Count, Case, When, IntegerField, Max, F, Q
from django.db.models import Window

from django.db.models.functions import Lag, ExtractDay

import logging
import datetime

logger = logging.getLogger(__name__)

@extend_schema_view(
    ticket_add=SWAGGER_TICKETS_ADD,
    ticket_upd=SWAGGER_TICKETS_UPD,
    ticket_del=SWAGGER_TICKETS_DEL,
    ticket_list=SWAGGER_TICKETS_LIST,
    ticket_reaction=SWAGGER_TICKETS_REACTION,
    ticket_detail=SWAGGER_TICKETS_DETAIL,
    ticket_favorite=SWAGGER_TICKETS_FAVORITE,
    win_rate_calculation=SWAGGER_WIN_RATE_CALCULATION,
    weekday_most_win=SWAGGER_WEEKDAY_MOST_WIN,
    ballpark_most_win=SWAGGER_BALLPARK_MOST_WIN,
    opponent_most_win=SWAGGER_OPPONENT_MOST_WIN,
    longest_winning_streak=SWAGGER_LONGEST_WINNING_STREAK,
    win_site_percent=SWAGGER_WIN_SITE_PERCENT,
    win_home_percent=SWAGGER_WIN_HOME_PERCENT,
)

class TicketsViewSet(
    GenericViewSet,
):

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])  # 직관 일기 리스트로 보기
    def ticket_list(self, request):
        try:
            user = request.user
            queryset = Ticket.objects.all()
            team_id = self.request.query_params.get("team_id")
            favorite = self.request.query_params.get("favorite")

            if team_id: # 팀 확인 시
                try:
                    if favorite == 'true': # 최애 경기 보고 싶을 경우
                        queryset = queryset.filter(ballpark_id=team_id, favorite=True, writer=user)
                    elif favorite == 'false':
                        queryset = queryset.filter(ballpark_id=team_id, favorite=False, writer=user)
                    else:
                        queryset = queryset.filter(ballpark_id=team_id, writer=user)
                except ValueError:
                    pass
            else: # 팀 미확인 시
                try:
                    if favorite == 'true':
                        queryset = queryset.filter(favorite=True, writer=user)
                    elif favorite == 'false':
                        queryset = queryset.filter(favorite=False, writer=user)
                    else:
                        queryset = queryset.filter(writer=user)
                except ValueError:
                    pass

            serializer = TicketListSerializer(queryset, many=True)  # 쿼리셋 직렬화
            return Response(serializer.data)

        except Exception as e:
            logger.error(f"Error occurred in ticket_list: {e}")
            return Response({'error': str(e)}, status=500)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])  # 티켓 상세 보기
    def ticket_detail(self, request):
        user = request.user
        ticket_id = request.query_params.get('id')
        if not ticket_id:
            return Response({"detail": "티켓id값이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ticket = Ticket.objects.get(id=ticket_id,writer=user)  # 해당 ID의 티켓 객체 가져오기
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TicketSerializer(ticket)  # 티켓 직렬화
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def ticket_add(self, request):
        user = request.user
        try:
            game_id = request.data.get('game')
            try:
                game = Game.objects.get(id=game_id)
                date = game.game_date
                ballpark_id = game.ballpark.id
                opponent_id = game.team_away.id
            except Game.DoesNotExist:
                return Response({'error': 'Invalid game ID'}, status=400)

            data = request.data.copy()
            data['game'] = game_id

            serializer = TicketAddSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save(writer=user,ballpark=ballpark_id,opponent=opponent_id,date=date)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=400)
        except Exception as e:
            logger.error(f"Error occurred in ticket_add: {e}")
            return Response({'error': str(e)}, status=500)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])  # 티켓 일기 수정하기
    def ticket_upd(self, request):
        try:
            ticket_identifier = request.data.get('id')
            if not ticket_identifier:
                return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                ticket = Ticket.objects.get(id=ticket_identifier)
            except Ticket.DoesNotExist:
                return Response({"detail": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = TicketAddSerializer(ticket, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=400)

        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated]) # 티켓 삭제
    def ticket_del(self, request):
        ticket_id = request.data.get('id')
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

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated]) #티켓에 반응 추가/삭제하기
    def ticket_reaction(self, request):
        user = request.user
        ticket_identifier = request.data.get('id')
        reaction_pos = request.data.get("reaction_pos")
        reaction_type = request.data.get("reaction_type")

        # ticket_identifier에 해당하는 티켓 객체 조회
        try:
            ticket = Ticket.objects.get(id=ticket_identifier)
        except Ticket.DoesNotExist:
            return Response({'message': '티켓을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # 티켓의 작성자가 현재 id일 경우 service 접근 금지
        if ticket.writer.id == user.id:
            return Response({'message': '자신의 티켓에는 반응을 추가/삭제할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        service = TicketService()

        if reaction_pos == "add": # 반응 추가
            service.add_reaction(ticket_identifier,reaction_type)
            message = "반응 추가 성공"
        elif reaction_pos == "del": # 반응 삭제
            service.del_reaction(ticket_identifier,reaction_type)
            message = "반응 삭제 성공"
        else:
            return Response({'message': '잘못된 요청입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        response_data = {
            'message': message,
            'ticket_id': ticket_identifier,
            'reaction_pos': reaction_pos
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated]) #최애경기 티켓 선정
    def ticket_favorite(self, request):
        try:
            ticket_id = request.data.get('id')
            favorite_status = request.data.get('favorite_status')
        except KeyError:
            return Response({"error": "요청 데이터에 'id'와 'set_favorite' 값이 필요합니다."}, status=400)

        service = TicketService()
        service.set_favorite(ticket_id,favorite_status)
        message = "적용 성공"

        response_data = {
            'message': message,
            'ticket_id': ticket_id,
            'favorite_status': favorite_status
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated]) # 경기 결과 통계 추산
    def win_rate_calculation(self, request):
        user = request.user
        queryset = Ticket.objects.filter(writer=user).aggregate(
            win_count=Count(Case(When(result='승리', then=1), output_field=IntegerField())),
            loss_count=Count(Case(When(result='패배', then=1), output_field=IntegerField())),
            draw_count=Count(Case(When(result='무승부', then=1), output_field=IntegerField())),
            cancel_count=Count(Case(When(result='취소', then=1), output_field=IntegerField())),
        )
        return Response(queryset)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated]) # 가장 승리 많이 한 요일 산출
    def weekday_most_win(self, request):
        user = request.user
        queryset = Ticket.objects.filter(writer=user, result="승리")

        service = TicketService()
        most_wins_day = service.calculate_weekday_wins(queryset)

        return Response({'most_wins_day': most_wins_day})

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])  # 가장 승리 많이한 구장 산출
    def ballpark_most_win(self, request):
        user = request.user
        queryset = Ticket.objects.filter(writer=user, result="승리")

        service = TicketService()
        most_wins_ballpark = service.calculate_most_win_ballpark(queryset)

        return Response({"most_wins_ballpark": most_wins_ballpark})

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated]) # 가장 상대로 승리 많이한 구단 산출
    def opponent_most_win(self, request):
        user = request.user
        queryset = Ticket.objects.filter(writer=user, result="승리")

        service = TicketService()
        most_wins_opponent = service.calculate_most_win_opponent(queryset)

        return Response({"most_wins_opponent" : most_wins_opponent})

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])  # 가장 긴 연승 기간 찾기
    def longest_winning_streak(self, request):
        user = request.user

        # 티켓 승리 내역 가져오기
        queryset = Ticket.objects.filter(writer=user, result="승리").annotate(
            prev_date=Window(
                expression=Lag('date', 1),
                partition_by=[F('writer')],
                order_by=F('date').asc()
            )
        ).order_by('date')

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

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated]) # 직관 경기 승률 퍼센티지 추산
    def win_site_percent(self, request):
        user = request.user
        queryset = Ticket.objects.filter(writer=user, is_ballpark=True)

        total_games = queryset.count()
        wins = queryset.filter(result="승리").count()

        if total_games == 0:
            win_percent = 0
        else:
            win_percent = int((wins / total_games) * 100)

        return Response(win_percent)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated]) # 집관 경기 승률 퍼센티지 추산
    def win_home_percent(self, request):
        user = request.user
        queryset = Ticket.objects.filter(writer=user, is_ballpark=False)

        total_games = queryset.count()
        wins = queryset.filter(result="승리").count()

        if total_games == 0:
            win_percent = 0
        else:
            win_percent = int((wins / total_games) * 100)

        return Response(win_percent)

