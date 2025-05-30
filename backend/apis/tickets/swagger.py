from http.client import responses

from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework import serializers

from apis.tickets.serializers import TicketSerializer
from apis.tickets.serializers import TicketListSerializer
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
    description="확인하고자 하는 티켓의 id를 입력시켜주세요.",
    required=False,
)

QUERY_PARAMETER_CALENDAR_TYPE = OpenApiParameter(
    name="date",
    type=str,
    location=OpenApiParameter.QUERY,
    description="확인하고자 하는 date값(YYYY-MM-DD)을 입력시켜주세요. (캘린더 화면 접근시 id값 제외 하고서 date만 입력해주세요)",
    required=False,
)

QUERY_PARAMETER_CALENDAR_USER_TYPE = OpenApiParameter(
    name="user_id",
    type=str,
    location=OpenApiParameter.QUERY,
    description="확인하고자 하는 유저 ID를 입력시켜주세요. (user_id값은 따로 확인해서 기입이 필요합니다.)",
    required=False,
)

QUERY_PARAMETER_TARGET_ID_TYPE = OpenApiParameter(
    name="target_id",
    type=str,
    location=OpenApiParameter.QUERY,
    description="해당 하는 ID를 입력해주세요 본인일 경우 본인의 ID 친구일 경우 보고 싶은 티켓의 ID값을 입력해주시면 됩니다.",
    required=False,
)

SWAGGER_TICKETS_FIND_FAVORITE = OpenApiParameter(
    name="favorite",
    type=str,
    location=OpenApiParameter.QUERY,
    description="최애 경기를 확인하고 싶은 경우 해당 값에 True를 넣어주세요.",
    default=False,
    required=False,
)

SWAGGER_TICKETS_FIND_CHEER = OpenApiParameter(
    name="is_cheer",
    type=str,
    location=OpenApiParameter.QUERY,
    description="타팀 경기를 확인하고 싶은 경우 해당 값에 True를 넣어주세요.",
    default=False,
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
        SWAGGER_TICKETS_FIND_CHEER,
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
    parameters=[
        QUERY_PARAMETER_DETAIL_TYPE,
        QUERY_PARAMETER_CALENDAR_TYPE,
        QUERY_PARAMETER_TARGET_ID_TYPE,
    ],
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
    description="내 직관일기를 등록합니다. (직접입력, 자동입력 통합)",
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "date": {"type": "string"},
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
                "hometeam_id": {"type": "integer"},
                "awayteam_id": {"type": "integer"},
                "direct_yn": {"type": "boolean"},
                "is_cheer": {"type", "boolean"},
            }
        }
    },
    examples=[
        OpenApiExample(
            name="Example",
            summary="Example input",
            description="직관 일기 입력 예시입니다. \n ",
            value={
                "date": "2025-08-21",
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
                "hometeam_id": 1,
                "awayteam_id": 6,
                "direct_yn": False,
                "is_cheer": False,
            }
        )
    ],
    responses={200: OpenApiTypes.OBJECT},
)


SWAGGER_TICKETS_UPD = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 일기 수정",
    description="내 직관일기를 수정합니다.",
    request={
        "multipart/form-data": {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
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
                "hometeam_id": {"type": "string"},
                "awayteam_id": {"type": "string"},
                "is_cheer": {"type": "boolean"},
            }
        }
    },
    examples=[
        OpenApiExample(
            name="Example",
            summary="Example input",
            description="티켓 일기 입력(수정) 예시입니다. \n"
                        "direct_home_team과 direct_away_team경우에는 direct_yn 이 True일 경우에만 기입필요",
            value={
                "id":1,
                "result": "패배",
                "weather": "맑음",
                "is_ballpark": False,
                "score_our":2,
                "score_opponent":7,
                "starting_pitchers": "김광현",
                "gip_place": "제 집이요",
                "image": "",
                "food": "피자",
                "memo": "재미없었다",
                "is_homeballpark":False,
                "only_me": True,
                "is_double": True,
                "hometeam_id": {"type": "integer"},
                "awayteam_id": {"type": "integer"},
                "is_cheer": False,
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

SWAGGER_TICKETS_REACTION_VIEW = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="지정 티켓 반응 보기",
    parameters=[
        QUERY_PARAMETER_TARGET_ID_TYPE,
    ],
    description="지정된 티켓의 반응 갯수가 몇개 있는지 노출합니다.",
    responses={
        200: OpenApiExample(
            "Success Response", value=[], response_only=True, status_codes=["200"]
        ),
    },
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
            description="티켓 반응 추가하거나 삭제하는 예시입니다. \n reaction_pos는 추가 시 add 삭제 시 del 기입 ",
            value={
                "id": 1,
                "reaction_pos": "add",
                "reaction_type": "rage",
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
                "is_ballpark_win_rate": {
                    "win_count": 1,
                    "loss_count": 0,
                    "draw_count": 0,
                    "cancel_count": 0
                },
                "is_not_ballpark_win_rate": {
                    "win_count": 0,
                    "loss_count": 2,
                    "draw_count": 0,
                    "cancel_count": 0
                }
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

SWAGGER_BALLPARK_MOST_VIEW = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="최다 관람 구장 표출",
    description="그동안 가장 많이 티켓을 남긴 구단을 보여줍니다",
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            name="Example",
            summary="Example input",
            description="티켓 확인하여 가장 관람이력이 많은 구장 명 출력",
            value={"most_wins_ballpark": "창원NC파크"}
        ),
    ],
)

SWAGGER_OPPONENT_MOST_WIN = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="최다 상대 승리 구단 표출",
    description="그동안 티켓들의 가장 승리가 많은 상대 구단을 보여줍니다",
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            name="Example",
            summary="Example input",
            description="승리 티켓 확인하여 가장 상대방으로 승리가 많은 팀 명 출력",
            value={"most_wins_opponent": "롯데 자이언츠"}
        ),
    ],
)

SWAGGER_LONGEST_WINNING_STREAK = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="가장 긴 연승구간 표출",
    description="티켓 들중 연승구간이 가장 긴 횟수를 보여줍니다",
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            name="Example",
            summary="Example input",
            description="연승기간 계산하여 숫자로 출력",
            value={
                "longest_winning_streak" : 2,
            }
        ),
    ],
)

QUERY_PARAMETER_IS_BALLPARK_TYPE = OpenApiParameter(
    name="is_ballpark",
    type=str,
    location=OpenApiParameter.QUERY,
    description="직관인지 집관인지 값을 통해 구분해주세요. 직관일 경우 True , 집관일 경우 False",
    required=False,
)

SWAGGER_WIN_PERCENT = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="직관 승률 표출",
    description="직관으로 찍은 티켓의 총 승률을 계산합니다",
    responses={200: OpenApiTypes.OBJECT},
    parameters=[QUERY_PARAMETER_IS_BALLPARK_TYPE],
    examples=[
        OpenApiExample(
            name="Example",
            summary="Example input",
            description="승률 계산하여 퍼센티지 숫자로 출력 (% 기호는 제외)",
            value={50}
        ),
    ],
)

QUERY_PARAMETER_CALENDAR_TYPE = OpenApiParameter(
    name="date",
    type=str,
    location=OpenApiParameter.QUERY,
    description="확인하고자 하는 달을 입력해주세요(YYYY-MM)",
    required=False,
)

SWAGGER_TICKETS_CALENDAR_LOG = extend_schema(
    tags=SWAGGER_TICKETS_TAGS,
    summary="해당하는 달의 직관 일기 내역 노출",
    description="선택한 달의 직관 일기 내역을 노출합니다",
    responses={200: OpenApiTypes.OBJECT},
    request=TicketSerializer,
    parameters=[
        QUERY_PARAMETER_CALENDAR_TYPE,
        QUERY_PARAMETER_CALENDAR_USER_TYPE,
    ],
    examples=[
        OpenApiExample(
            name="Example",
            summary="Example input",
            description="opponent는 홈구장 기준 상대편 ballpark는 홈구장 기준 본인기준입니다",
            value={
                "id": 25,
                "date": "2024-08-20",
                "result": "승리",
                "writer_id": 2,
                "game_id": 622,
                "opponent": {
                    "id": 6,
                    "name": "SSG 랜더스"
                },
                "ballpark": {
                    "id": 5,
                    "name": "수원 케이티 위즈 파크",
                    "team_id": 5
                }
            },
        ),
    ],
)

SWAGGER_TICKETS_DIRECT_ADD = extend_schema(
 tags=SWAGGER_TICKETS_TAGS,
 summary="직관 일기 직접 등록",
 description="내 직관일기를 직접 등록합니다.(팀명)",
 request={
     "multipart/form-data": {
         "type": "object",
         "properties": {
             "date": {"type": "string"},
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
             "direct_home_team": {"type": "string"},
             "direct_away_team": {"type": "string"},
             "is_cheer_home": {"type": "boolean"},
         }
     }
 },
 examples=[
     OpenApiExample(
         name="Example",
         summary="Example input",
         description="직관 일기 직접 입력 예시입니다. \n ",
         value={
             "date": "2025-08-21",
             "result": "승리",
             "weather": "흐림",
             "is_ballpark": True,
             "score_our":9,
             "score_opponent":6,
             "starting_pitchers": "원태인",
             "gip_place": "",
             "image": "",
             "food": "닭강정",
             "memo": "재미있었다",
             "is_homeballpark":True,
             "only_me": False,
             "is_double": False,
             "direct_home_team": "SSG랜더스",
             "direct_away_team": "KT위즈",
             "is_cheer_home": True,
         }
     )
 ],
 responses={200: OpenApiTypes.OBJECT},
)
