from http.client import responses

from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

from apis.tickets.serializers import TicketSerializer
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
    summary="직관 일기 등록",
    description="내 직관일기를 등록합니다.",
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "game": {"type": "integer"},
                "result": {"type": "string"},
                "weather": {"type": "string"},
                "is_ballpark": {"type": "boolean"},
                "score_our": {"type": "integer"},
                "score_opponent": {"type": "integer"},
                "starting_pitchers": {"type": "string"},
                "gip_place": {"type": "string"},
                "image": {"type": "string", "format": "binary"},
                "food": {"type": "string"},
                "memo": {"type": "string"},
                "is_homeballpark": {"type": "boolean"},
                "only_me": {"type": "boolean"},
                "is_double": {"type": "boolean"},
            }
        }
    },
    examples=[
        OpenApiExample(
            name="Example",
            summary="Example input",
            description="직관 일기 입력 예시입니다. \n "
                        "경기일정에서 받아와야 하는 값"
                        "game_id -> game",
            value={
                "game": 624,
                "result": "승리",
                "weather": "흐림",
                "is_ballpark": True,
                "score_our":9,
                "score_opponent":6,
                "starting_pitchers": "고우석",
                "gip_place": "",
                "image": "",
                "food": "닭강정",
                "memo": "재미있었다",
                "is_homeballpark":True,
                "only_me": False,
                "is_double": False,
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
                "result": "패배",
                "weather": "맑음",
                "is_ballpark": True,
                "score_our":2,
                "score_opponent":7,
                "starting_pitchers": "김광현",
                "gip_place": "",
                "food": "닭강정",
                "memo": "재미있었다",
                "is_homeballpark":True,
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
        OpenApiExample(
            name="Example 4",
            summary="Example input",
            description="승리 횟수, 패배 횟수, 무승부 횟수, 취소 횟수를 int로 출력합니다",
            value={
              "win_count": 2,
              "loss_count": 0,
              "draw_count": 0,
              "cancel_count": 0
            }
        ),
    ],
)

SWAGGER_WEEKDAY_MOST_WIN = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="최다 승리 요일 표출",
    description="그동안 티켓들의 가장 승리가 많은 요일을 보여줍니다",
    responses={200: OpenApiTypes.OBJECT},
    examples=[

    ],
)

SWAGGER_BALLPARK_MOST_WIN = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="최다 승리 구장 표출",
    description="그동안 티켓들의 가장 승리가 많은 구장을 보여줍니다",
    responses={200: OpenApiTypes.OBJECT},
    examples=[

    ],
)

SWAGGER_OPPONENT_MOST_WIN = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="최다 상대 승리 구단 표출",
    description="그동안 티켓들의 가장 승리가 많은 상대 구단을 보여줍니다",
    responses={200: OpenApiTypes.OBJECT},
    examples=[

    ],
)

SWAGGER_LONGEST_WINNING_STREAK = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="가장 긴 연승구간 표출",
    description="티켓 들중 연승구간이 가장 긴 횟수를 보여줍니다",
    responses={200: OpenApiTypes.OBJECT},
    examples=[

    ],
)

SWAGGER_WIN_SITE_PERCENT = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 승률 표출",
    description="직관으로 찍은 티켓의 총 승률을 계산합니다",
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            name="Example",
            summary="Example input",
            description="승률 계산하여 퍼센티지 숫자로 출력 (% 기호는 제외)",
            value={
                50
            }
        ),
    ],
)

SWAGGER_WIN_HOME_PERCENT = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="집관 승률 표출",
    description="집관으로 찍은 티켓의 총 승률을 계산합니다",
    responses={200: OpenApiTypes.OBJECT},
    examples=[

    ],
)