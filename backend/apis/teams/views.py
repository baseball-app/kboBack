from drf_spectacular.utils import extend_schema_view
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apis.teams.serializers import TeamsSerializer
from apis.teams.swagger import SWAGGER_TEAMS_LIST
from apps.teams.models import Team
from base.mixins import SentryLoggingMixin


@extend_schema_view(
    list=SWAGGER_TEAMS_LIST,
)
class TeamsViewSet(
    SentryLoggingMixin,
    ListModelMixin,
    GenericViewSet,
):
    permission_classes = [
        IsAuthenticated,
    ]

    queryset = Team.objects.all()
    serializer_class = TeamsSerializer
    pagination_class = None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data["last_page"] = self.paginator.page.paginator.num_pages  # 수정된 부분
            return response

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
