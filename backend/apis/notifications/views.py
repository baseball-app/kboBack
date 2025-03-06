from drf_spectacular.utils import extend_schema_view
from rest_framework.mixins import (
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apis.notifications.serializers import NotificationSerializer
from apis.notifications.swagger import SWAGGER_NOTIFICATIONS_LIST, SWAGGER_NOTIFICATIONS_UPDATE
from apps.notifications.models import Notification
from base.mixins import SentryLoggingMixin


@extend_schema_view(
    list=SWAGGER_NOTIFICATIONS_LIST,
    update=SWAGGER_NOTIFICATIONS_UPDATE,
)
class NotificationsViewSet(
    SentryLoggingMixin,
    ListModelMixin,
    UpdateModelMixin,
    GenericViewSet,
):
    permission_classes = [
        IsAuthenticated,
    ]

    serializer_class = NotificationSerializer

    def get_queryset(self):
        if self.action == "list":
            friends = self.request.user.friendships_source.values_list("target", flat=True)
            target_ids = [self.request.user.id] + [friends]

            return Notification.objects.filter(user__id__in=target_ids)
        return Notification.objects.filter(user=self.request.user)

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

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        data = request.data.copy()
        data["user"] = request.user.id

        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
