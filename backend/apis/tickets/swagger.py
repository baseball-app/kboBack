from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from rest_framework import serializers

from apis.tickets.serializers import TicketSerializer

SWAGGER_TICKETS_TAGS = ["tickets"]

QUERY_PARAMETER_READ_TYPE = OpenApiParameter(
    name="id",
    type=str,
    location=OpenApiParameter.QUERY,
    description="티켓 정보 읽기",
    required=False,
)

SWAGGER_TICKETS_LIST = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 조회",
    parameters=[QUERY_PARAMETER_READ_TYPE],
    description="직관 일기 조회 목록 표출",
)

SWAGGER_TICKETS_ADD = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 추가",
    description="내 직관일기를 추가합니다.",
)

SWAGGER_TICKETS_UPD = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 수정",
    description="내 직관일기를 수정합니다.",
)

SWAGGER_TICKETS_DEL = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 삭제",
    description="내 직관일기를 삭제합니다.",
)

SWAGGER_TICKETS_DOUBLE_ADD = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 추가(더블헤더)",
    description="내 직관일기를 추가합니다.",
)
