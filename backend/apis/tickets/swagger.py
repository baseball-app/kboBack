from http.client import responses

from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

from apis.tickets.serializers import TicketSerializer, TicketFavoriteSerializer
from apis.tickets.serializers import TicketListSerializer
from apis.tickets.serializers import TicketUpdSerializer
from apis.tickets.serializers import TicketReactionSerializer
from apis.tickets.serializers import TicketDelSerializer
from apis.tickets.serializers import TicketFavoriteSerializer

SWAGGER_TICKETS_TAGS = ["tickets"]

QUERY_PARAMETER_LIST_TYPE = OpenApiParameter(
    name="team_id",
    type=str,
    location=OpenApiParameter.QUERY,
    description="확인하고자 하는 team id를 입력시켜주세요(return 값의 ballpark_id 와 동일)",
    required=False,
)

QUERY_PARAMETER_DETAIL_TYPE = OpenApiParameter(
    name="id",
    type=str,
    location=OpenApiParameter.QUERY,
    description="확인하고자 하는 ticket_id를 입력시켜주세요. (티켓 추가 작업 후 확인 가능)",
    required=False,
)

SWAGGER_TICKETS_FIND_FAVORITE = OpenApiParameter(
    name="favorite",
    type=str,
    location=OpenApiParameter.QUERY,
    description="최애 경기를 확인하고 싶은 경우 해당 값에 True를 넣어주세요.",
    default=True,
    required=False,
)

SWAGGER_TICKETS_LIST = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 조회",
    description="직관 일기 조회 목록 표출",
    request=TicketListSerializer,
    parameters=[
        QUERY_PARAMETER_LIST_TYPE,
        SWAGGER_TICKETS_FIND_FAVORITE,
    ],
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

SWAGGER_TICKETS_ADD = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 추가",
    description="내 직관일기를 추가합니다.",
    request=TicketSerializer,
    examples=[
        OpenApiExample(
            name="Example 1",
            summary="Example input",
            description="티켓 일기 입력 예시입니다. \n ballpark값과 opponent 값은 경기 일정에서 request로 받아와야 하는 값 \n "
                        "writer는 유저 인증값에서 가지고 와야 하는 값(현재 인증 해제)",
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
                "ballpark": 1,
                "opponent": 1,
            }
        )
    ],
    responses={200: OpenApiTypes.OBJECT},
)

SWAGGER_TICKETS_DOUBLE_ADD = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 추가(더블헤더)",
    description="직관 일기 입력 예시입니다.(일반 케이스와 동일)",
    request=TicketSerializer,
    examples=[
        OpenApiExample(
            name="Example 2",
            summary="Example input",
            description="직관 일기(더블헤더) 입력 예시입니다. \n ballpark값과 opponent 값은 경기 일정에서 request로 받아와야 하는 값 \n "
                        "writer는 유저 인증값에서 가지고 와야 하는 값(현재 인증 해제)",
            value={
                "date": "2025-05-05",
                "result": "패배",
                "weather": "바람",
                "is_ballpark": True,
                "score_our":1,
                "score_opponent":7,
                "starting_pitchers": "박세웅",
                "gip_place": "",
                "food": "치킨",
                "memo": "재미없었다",
                "is_homeballpark":True,
                "only_me": False,
                "ballpark": 1,
                "opponent": 1,
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
    request=TicketDelSerializer,
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            name="Example 1",
            summary="Example input",
            description="티켓 삭제 예시입니다",
            value={
                "id": 1,
            }
        ),
    ],
)

SWAGGER_TICKETS_REACTION = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 반응 추가",
    description="직관 일기에 대한 반응을 추가합니다",
    request=TicketReactionSerializer,
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            name="Example 4",
            summary="Example input",
            description="티켓 반응 추가하거나 삭제하는 예시입니다. \n reaction_pos는 추가 시 add 삭제 시 del 기입 , "
                        "\n reaction_type는 like,love,haha,yay,wow,sad,angry 기입 가능",
            value={
                "id": 1,
                "reaction_pos": "add",
                "reaction_type": "like",
            }
        ),
    ],
)

SWAGGER_TICKETS_FAVORITE = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 최애 경기 선정 및 해제",
    description="직관 일기 중 최애 경기를 추가하거나 해제할 수 있습니다",
    request=TicketFavoriteSerializer,
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            name="Example 4",
            summary="Example input",
            description="favorite_status 값이 clear일경우 최애 경기 해제, excute일경우 최애 경기 선정",
            value={
                "id": 1,
                "favorite_status": "excute",
            }
        ),
    ]
)

SWAGGER_WIN_RATE_CALCULATION = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="티켓 경기 결과 표출",
    description="그동안 티켓들의 총 승,무,패 기록을 확인할 수 있습니다",
    responses={200: OpenApiTypes.OBJECT},
    examples=[
    ],
)
