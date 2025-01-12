from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apis.tickets.serializers import TicketSerializer
from apis.tickets.swagger import SWAGGER_TICKETS_ADD, SWAGGER_TICKETS_UPD, SWAGGER_TICKETS_DEL, SWAGGER_TICKETS_LIST, SWAGGER_TICKETS_DOUBLE_ADD
from apps.tickets.models import Ticket

@extend_schema_view(
    ticketAdd=SWAGGER_TICKETS_ADD,
    ticketUpd=SWAGGER_TICKETS_UPD,
    ticketDel=SWAGGER_TICKETS_DEL,
    ticketList=SWAGGER_TICKETS_LIST,
    ticketDouAdd=SWAGGER_TICKETS_DOUBLE_ADD,
)

class TicketsViewSet(
    GenericViewSet,
):
    permission_classes = [
        AllowAny,
    ]

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def ticketList(self, request):
        user = request.user
        queryset = Ticket.objects.filter(writer=user)
        serializer = TicketSerializer(queryset, many=True)  # 쿼리셋 직렬화
        return Response(serializer.data)

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