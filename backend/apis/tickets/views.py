from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apis.tickets.serializers import TicketSerializer
from apps.tickets.models import Ticket

class TicketsViewSet(
    GenericViewSet,
):
    permission_classes = [
        AllowAny,
    ]

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def ticketListView(self, request):
        user = request.user
        queryset = Ticket.objects.filter(writer=user)
        serializer = TicketSerializer(queryset, many=True)  # 쿼리셋 직렬화
        return Response(serializer.data)
