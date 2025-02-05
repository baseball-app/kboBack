from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.shortcuts import get_object_or_404

from apis.tickets.serializers import TicketSerializer
from apis.tickets.swagger import SWAGGER_TICKETS_ADD, SWAGGER_TICKETS_UPD, SWAGGER_TICKETS_DEL, SWAGGER_TICKETS_LIST, SWAGGER_TICKETS_DOUBLE_ADD, SWAGGER_TICKETS_REACTION, SWAGGER_TICKETS_DETAIL, SWAGGER_WIN_RATE_CALCULATION
from apps.tickets.models import Ticket

from .service import TicketReactionService
from django.db.models import Count, Case, When, IntegerField

@extend_schema_view(
    ticketAdd=SWAGGER_TICKETS_ADD,
    ticketUpd=SWAGGER_TICKETS_UPD,
    ticketDel=SWAGGER_TICKETS_DEL,
    ticketList=SWAGGER_TICKETS_LIST,
    ticketDouAdd=SWAGGER_TICKETS_DOUBLE_ADD,
    ticketReaction=SWAGGER_TICKETS_REACTION,
    ticketDetail=SWAGGER_TICKETS_DETAIL,
    winratecalculation=SWAGGER_WIN_RATE_CALCULATION,
)

class TicketsViewSet(
    GenericViewSet,
):
    permission_classes = [
        AllowAny,
    ]

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated]) # 티켓 일렬로 보기
    def ticketList(self, request):
        user = request.user
        queryset = Ticket.objects.filter(writer=user)
        serializer = TicketSerializer(queryset, many=True)  # 쿼리셋 직렬화
        return Response(serializer.data)

    @action(methods=["GET"], detail=True, permission_classes=[IsAuthenticated])  # 티켓 상세 보기
    def ticketDetail(self, request, pk=None):
        user = request.user
        ticket = get_object_or_404(Ticket, pk=pk, writer=user)  # 특정 티켓 조회 및 작성자 확인
        serializer = TicketSerializer(ticket)  # 티켓 직렬화
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated]) #일반 스케줄 시 등록 경우
    def ticketAdd(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def ticketUpd(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def ticketDel(self, request):
        ticket = Ticket.objects.get(id=request.data['id'])
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated]) # 더블헤더 진행 시 등록 경우
    def ticketDouAdd(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated]) #티켓에 반응 추가하기
    def ticketReaction(self, request, pk=None):
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
    def winratecalculation(self, request):
        user = request.user
        queryset = Ticket.objects.filter(writer=user).aggregate(
            win_count=Count(Case(When(result='승리', then=1), output_field=IntegerField())),
            loss_count=Count(Case(When(result='패배', then=1), output_field=IntegerField())),
            draw_count=Count(Case(When(result='무승부', then=1), output_field=IntegerField())),
            cancel_count=Count(Case(When(result='취소', then=1), output_field=IntegerField())),
        )
        return Response(queryset)


