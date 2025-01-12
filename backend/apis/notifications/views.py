from drf_spectacular.utils import extend_schema_view
from rest_framework.mixins import (
    ListModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apis.notifications.enums import NOTIFICATION_READ_TYPE
from apis.notifications.serializers import NotificationSerializer
from apis.notifications.swagger import SWAGGER_NOTIFICATIONS_LIST, SWAGGER_NOTIFICATIONS_UPDATE
from apps.notifications.models import Notification


@extend_schema_view(
    list=SWAGGER_NOTIFICATIONS_LIST,
    update=SWAGGER_NOTIFICATIONS_UPDATE,
)
class NotificationsViewSet(
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
            read_type = self.request.query_params.get("read_type", NOTIFICATION_READ_TYPE.ALL_NOTIFICATIONS)
            friends = self.request.user.friendships_source.values_list("target", flat=True)
            # 회의 때 알림 관련해서 여쭤보고 수정하기
            if read_type == NOTIFICATION_READ_TYPE.FRIEND_FEEDBACK_NOTIFICATION:
                target_ids = [self.request.user.id] + [friends]
            else:
                target_ids = [self.request.user.id] + [friends]

            return Notification.objects.filter(user__id__in=target_ids)
        return Notification.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

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
