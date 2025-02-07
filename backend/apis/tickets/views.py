from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.shortcuts import get_object_or_404

from apis.tickets.serializers import TicketSerializer
from apis.tickets.serializers import TicketListSerializer
from apis.tickets.serializers import TicketUpdSerializer
from apis.games.serializers import BallparkSerializer
from apis.games.serializers import GameSerializer

from apis.tickets.swagger import SWAGGER_TICKETS_ADD, SWAGGER_TICKETS_UPD, SWAGGER_TICKETS_DEL, SWAGGER_TICKETS_LIST, SWAGGER_TICKETS_DOUBLE_ADD, SWAGGER_TICKETS_REACTION, SWAGGER_TICKETS_DETAIL, SWAGGER_WIN_RATE_CALCULATION
from apps.tickets.models import Ticket
from apps.games.models import Game
from apps.games.models import Ballpark

from .service import TicketReactionService
from django.db.models import Count, Case, When, IntegerField

@extend_schema_view(
    ticket_add=SWAGGER_TICKETS_ADD,
    ticket_upd=SWAGGER_TICKETS_UPD,
    ticket_del=SWAGGER_TICKETS_DEL,
    ticket_list=SWAGGER_TICKETS_LIST,
    ticket_dou_add=SWAGGER_TICKETS_DOUBLE_ADD,
    ticket_reaction=SWAGGER_TICKETS_REACTION,
    ticket_detail=SWAGGER_TICKETS_DETAIL,
    win_rate_calculation=SWAGGER_WIN_RATE_CALCULATION,
)

class TicketsViewSet(
    GenericViewSet,
):

    @action(methods=["GET"], detail=False, permission_classes=[AllowAny])  # 티켓 일렬로 보기
    def ticket_list(self, request):
        queryset = Ticket.objects.all()
        team_id = self.request.query_params.get("team_id")

        if team_id:
            try:  # team_id 선택 시
                queryset = queryset.filter(ballpark_id=team_id)
            except ValueError:  # 초기화면일 경우 전체 출력
                serializer = TicketListSerializer(queryset, many=True)  # 쿼리셋 직렬화
                return Response(serializer.data)

        queryset = Ticket.objects.values('id', 'date', 'writer_id', 'game_id', 'opponent_id', 'ballpark_id')

        serializer = TicketListSerializer(queryset, many=True)  # 쿼리셋 직렬화
        return Response(serializer.data)

    #@action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated]) # 티켓 일렬로 보기(로그인 인증 버전)
    def ticket_list_non_test(self, request):
        user = request.user
        queryset = Ticket.objects.filter(writer=user)

        team_id = self.request.query_params.get("team_id")

        if team_id:
            try:  # team_id 선택 시
                queryset = queryset.filter(ballpark_id=team_id)
            except ValueError:  # 초기화면일 경우 전체 출력
                serializer = TicketListSerializer(queryset, many=True)  # 쿼리셋 직렬화
                return Response(serializer.data)

        queryset = queryset.select_related("writer", "game", "opponent", "ballpark","id")

        serializer = TicketListSerializer(queryset, many=True)  # 쿼리셋 직렬화
        return Response(serializer.data)

    @action(methods=["GET"], detail=False, permission_classes=[AllowAny])  # 티켓 상세 보기
    def ticket_detail(self, request):
        user = request.user

        ticket_id = request.query_params.get('id')
        if not ticket_id:
            return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ticket = Ticket.objects.get(id=ticket_id)  # 해당 ID의 티켓 객체 가져오기
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = TicketSerializer(ticket)  # 티켓 직렬화
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny]) #일반 스케줄 시 등록 경우
    def ticket_add(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            # ballpark 값을 강제로 설정하여 저장합니다(games와 연계 이전).
            ballpark = Ballpark.objects.get(id=1)
            # opponent 값을 강제로 설정하여 저장합니다(games와 연계 이전).
            opponent = Game.objects.get(team_away_id=1)
            serializer.save(ballpark=ballpark,opponent=opponent)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny]) # 더블헤더 진행 시 등록 경우
    def ticket_dou_add(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            # ballpark 값을 강제로 설정하여 저장합니다(games와 연계 이전).
            ballpark = Ballpark.objects.get(id=1)
            # opponent 값을 강제로 설정하여 저장합니다(games와 연계 이전).
            opponent = Game.objects.get(team_away_id=1)
            serializer.save(ballpark=ballpark,opponent=opponent,is_double=True)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny]) # 티켓 일기 수정하기
    def ticket_upd(self, request):
        ticket_identifier = request.data.get('id')
        if not ticket_identifier:
            return Response({"detail": "ID parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ticket = Ticket.objects.get(id=ticket_identifier)
        except Ticket.DoesNotExist:
            return Response({"detail": "Ticket not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TicketUpdSerializer(ticket, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny])
    def ticket_del(self, request):
        ticket = Ticket.objects.get(id=request.data['id'])
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny]) #티켓에 반응 추가하기
    def ticket_reaction(self, request, pk=None):
        ticket = get_object_or_404(Ticket, pk=pk)
        reaction_pos = request.data.get("reaction_pos")

        service = TicketReactionService()

        if reaction_pos == "add": # 반응 추가
            service.add_reaction(reaction_pos)
        elif reaction_pos == "del": # 반응 삭제
            service.del_reaction(reaction_pos)

        ticket.save()
        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=status.HTTP_200_OK)

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


