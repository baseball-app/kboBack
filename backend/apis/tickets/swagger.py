from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

from apis.tickets.serializers import TicketSerializer
from apis.tickets.serializers import TicketListSerializer
from apis.tickets.serializers import TicketUpdSerializer

SWAGGER_TICKETS_TAGS = ["tickets"]

QUERY_PARAMETER_LIST_TYPE = OpenApiParameter(
    name="team_id",
    type=str,
    location=OpenApiParameter.QUERY,
    description="확인하고자 하는 team id를 입력시켜주세요",
    required=False,
)

QUERY_PARAMETER_DETAIL_TYPE = OpenApiParameter(
    name="id",
    type=str,
    location=OpenApiParameter.QUERY,
    description="확인하고자 하는 ticket_id를 입력시켜주세요. (티켓 추가 작업 후 확인 가능)",
    required=False,
)

SWAGGER_TICKETS_LIST = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 조회",
    description="직관 일기 조회 목록 표출",
    request=TicketListSerializer,
    parameters=[QUERY_PARAMETER_LIST_TYPE],
    responses={
        200: OpenApiExample(
            "Success Response", value=[], response_only=True, status_codes=["200"]
        ),
    },
)

SWAGGER_TICKETS_DETAIL = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 상세 보기",
    parameters=[QUERY_PARAMETER_DETAIL_TYPE],
    description="직관 일기 상세 표기 표출",
    responses={
        200: OpenApiExample(
            "Success Response", value=[], response_only=True, status_codes=["200"]
        ),
    },
)

# 직관 일기 추가 용 모음
## 경기 결과
QUERY_PARAMETER_DATE = OpenApiParameter(
    name="date",
    type=str,
    location=OpenApiParameter.QUERY,
    description="경기 일정(형식: YYYY-MM-DD)",
    required=False,
)

QUERY_PARAMETER_RESULT = OpenApiParameter(
    name="result",
    type=str,
    location=OpenApiParameter.QUERY,
    description="경기 결과(승리,패배,무승부,경기 취소)",
    required=False,
)

QUERY_PARAMETER_WEATHER = OpenApiParameter(
    name="weather",
    type=str,
    location=OpenApiParameter.QUERY,
    description="경기 날씨(맑음,흐림,비,바람)",
    required=False,
)

QUERY_PARAMETER_IS_BALLPARK = OpenApiParameter(
    name="is_ballpark",
    type=str,
    location=OpenApiParameter.QUERY,
    description="시청 위치(직관 -True, 집관 -False)",
    default=True,
    required=False,
)

QUERY_PARAMETER_SCORE_OUR = OpenApiParameter(
    name="score_our",
    type=str,
    location=OpenApiParameter.QUERY,
    description="응원팀 스코어",
    default=0,
    required=False,
)

QUERY_PARAMETER_SCORE_OPPONENT = OpenApiParameter(
    name="score_opponent",
    type=str,
    location=OpenApiParameter.QUERY,
    description="상대팀 스코어",
    default=0,
    required=False,
)

QUERY_PARAMETER_STARTING = OpenApiParameter(
    name="starting_pitchers",
    type=str,
    location=OpenApiParameter.QUERY,
    description="선발 투수",
    required=False,
)

QUERY_PARAMETER_GIP = OpenApiParameter(
    name="gip",
    type=str,
    location=OpenApiParameter.QUERY,
    description="집관일 경우에만 장소 직접 입력",
    required=False,
)

QUERY_PARAMETER_FOOD = OpenApiParameter(
    name="food",
    type=str,
    location=OpenApiParameter.QUERY,
    description="음식",
    required=False,
)

QUERY_PARAMETER_MEMO = OpenApiParameter(
    name="memo",
    type=str,
    location=OpenApiParameter.QUERY,
    description="메모",
    required=False,
)

QUERY_PARAMETER_IS_HOME_BALLPARK = OpenApiParameter(
    name="is_ballpark",
    type=str,
    location=OpenApiParameter.QUERY,
    description="홈/원정 여부",
    default=True,
    required=False,
)

QUERY_PARAMETER_WRITER = OpenApiParameter(
    name="writer_id",
    type=str,
    location=OpenApiParameter.QUERY,
    description="등록자(로그인 id)",
    default=1,
    required=False,
)

QUERY_PARAMETER_ONLY_ME = OpenApiParameter(
    name="only_me",
    type=str,
    location=OpenApiParameter.QUERY,
    description="나만 보기 여부",
    default=False,
    required=False,
)

SWAGGER_TICKETS_ADD = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 추가",
    description="내 직관일기를 추가합니다.",
    request=TicketSerializer,
    parameters=[
        QUERY_PARAMETER_DATE,
        QUERY_PARAMETER_RESULT,
        QUERY_PARAMETER_WEATHER,
        QUERY_PARAMETER_IS_BALLPARK,
        QUERY_PARAMETER_SCORE_OUR,
        QUERY_PARAMETER_SCORE_OPPONENT,
        QUERY_PARAMETER_STARTING,
        QUERY_PARAMETER_GIP,
        QUERY_PARAMETER_FOOD,
        QUERY_PARAMETER_MEMO,
        QUERY_PARAMETER_IS_HOME_BALLPARK,
        QUERY_PARAMETER_WRITER,
        QUERY_PARAMETER_ONLY_ME,
    ],
    examples=[
        OpenApiExample(
            name="Example 1",
            summary="Example input",
            description="티켓 일기 입력 예시입니다.",
            value={
                "date": "2025-04-09",
                "result": "승리",
                "weather": "흐림",
                "is_ballpark": True,
                "score_our":9,
                "score_opponent":6,
                "starting_pitchers": "고우석",
                "gip_place": "",
                "food": "닭강정",
                "memo": "재미있었다",
                "is_homeballpark":True,
                "writer": 1,
                "only_me": True,
            }
        )
    ],
    responses={200: OpenApiTypes.OBJECT},
)

SWAGGER_TICKETS_DOUBLE_ADD = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 추가(더블헤더)",
    description="티켓 일기 입력 예시입니다.(일반 케이스와 동일)",
    request=TicketSerializer,
    parameters=[
        QUERY_PARAMETER_DATE,
        QUERY_PARAMETER_RESULT,
        QUERY_PARAMETER_WEATHER,
        QUERY_PARAMETER_IS_BALLPARK,
        QUERY_PARAMETER_SCORE_OUR,
        QUERY_PARAMETER_SCORE_OPPONENT,
        QUERY_PARAMETER_STARTING,
        QUERY_PARAMETER_GIP,
        QUERY_PARAMETER_FOOD,
        QUERY_PARAMETER_MEMO,
        QUERY_PARAMETER_IS_HOME_BALLPARK,
        QUERY_PARAMETER_WRITER,
        QUERY_PARAMETER_ONLY_ME,
    ],
    examples=[
        OpenApiExample(
            name="Example 1",
            summary="Example input",
            description="티켓 일기 입력 예시입니다.",
            value={
                "date": "2025-04-09",
                "result": "승리",
                "weather": "흐림",
                "is_ballpark": True,
                "score_our":9,
                "score_opponent":6,
                "starting_pitchers": "고우석",
                "gip_place": "",
                "food": "닭강정",
                "memo": "재미있었다",
                "is_homeballpark":True,
                "writer": 1,
                "only_me": True,
            }
        )
    ],
    responses={200: OpenApiTypes.OBJECT},
)

SWAGGER_TICKETS_UPD = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 수정",
    description="내 직관일기를 수정합니다.",
    request=TicketUpdSerializer,
    parameters=[
    ],
    examples=[
        OpenApiExample(
            name="Example 1",
            summary="Example input",
            description="티켓 일기 입력(수정) 예시입니다.",
            value={
                "id":1,
                "result": "승리",
                "weather": "흐림",
                "is_ballpark": True,
                "score_our":9,
                "score_opponent":6,
                "starting_pitchers": "고우석",
                "gip_place": "",
                "food": "닭강정",
                "memo": "재미있었다",
                "is_homeballpark":True,
                "writer": 1,
                "only_me": True,
            }
        )
    ],
    responses={200: OpenApiTypes.OBJECT},
)

SWAGGER_TICKETS_DEL = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 삭제",
    description="내 직관일기를 삭제합니다.",
)

SWAGGER_TICKETS_REACTION = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 반응 추가",
    description="직관 일기에 대한 반응을 추가합니다",
    responses={200: OpenApiTypes.OBJECT},
    examples=[

    ],
)

SWAGGER_WIN_RATE_CALCULATION = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="티켓 경기 결과 표출",
    description="그동안 티켓들의 총 승,무,패 기록을 확인할 수 있습니다",
    responses={200: OpenApiTypes.OBJECT},
    examples=[
    ],
)
