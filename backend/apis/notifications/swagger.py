from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from rest_framework import serializers

from apis.notifications.serializers import NotificationSerializer

SWAGGER_NOTIFICATIONS_TAGS = ["NOTIFICATIONS"]

QUERY_PARAMETER_READ_TYPE = OpenApiParameter(
    name="read_type",
    type=str,
    location=OpenApiParameter.QUERY,
    description="알림 읽기 유형 (ALL: 전체, FRIEND_FEEDBACK: 친구의 반응)",
    required=False,
)

BODY_PARAMETER_UPDATE_NOTIFICATION = inline_serializer(
    name="UpdateNotification",
    fields={
        "is_read": serializers.BooleanField(),
    },
)

# 페이지네이션 응답 형식을 위한 시리얼라이저
PAGINATED_NOTIFICATION_RESPONSE = inline_serializer(
    name="PaginatedNotificationResponse",
    fields={
        "count": serializers.IntegerField(),
        "next": serializers.URLField(allow_null=True),
        "previous": serializers.URLField(allow_null=True),
        "results": NotificationSerializer(many=True),
        "last_page": serializers.IntegerField(),
    },
)

SWAGGER_NOTIFICATIONS_LIST = extend_schema(
    tags=SWAGGER_NOTIFICATIONS_TAGS,
    summary="알림 목록 조회",
    description="현재 사용자의 알림 목록을 조회합니다. 친구의 알림과 전체 알림을 선택적으로 필터링할 수 있습니다.",
    # parameters=[QUERY_PARAMETER_READ_TYPE],
    responses={200: PAGINATED_NOTIFICATION_RESPONSE},
)

SWAGGER_NOTIFICATIONS_UPDATE = extend_schema(
    tags=SWAGGER_NOTIFICATIONS_TAGS,
    summary="알림 업데이트",
    description="특정 알림의 읽음 상태를 업데이트합니다.",
    request=BODY_PARAMETER_UPDATE_NOTIFICATION,
    responses={200: NotificationSerializer},
)
