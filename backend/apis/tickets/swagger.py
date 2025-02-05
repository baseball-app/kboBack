from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from rest_framework import serializers

from apis.tickets.serializers import TicketSerializer

SWAGGER_TICKETS_TAGS = ["tickets"]

QUERY_PARAMETER_READ_TYPE = OpenApiParameter(
    name="id",
    type=str,
    location=OpenApiParameter.QUERY,
    description="티켓 소지 유저 확인",
    required=False,
)

QUERY_PARAMETER_READ_DETAIL_TYPE = OpenApiParameter(
    name="ticket",
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

SWAGGER_TICKETS_DETAIL = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 상세 보기",
    parameters=[QUERY_PARAMETER_READ_DETAIL_TYPE],
    description="직관 일기 상세 표기 표출",
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

SWAGGER_TICKETS_REACTION = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 반응 추가",
    description="직관 일기에 대한 반응을 추가합니다",
)

SWAGGER_WIN_RATE_CALCULATION = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="티켓 경기 결과 표출",
    description="그동안 티켓들의 총 승,무,패 기록을 확인할 수 있습니다",
)
