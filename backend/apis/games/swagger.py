from drf_spectacular.utils import extend_schema, OpenApiParameter

from apis.games.serializers import GameSerializer

SWAGGER_GAMES_TAGS = ["GAMES"]

QUERY_PARAMETER_START_DATE = OpenApiParameter(
    name="start_date",
    type=str,
    location=OpenApiParameter.QUERY,
    description="경기 일정 조회 시작일 (형식: YYYY-MM-DD)",
    required=False,
)

QUERY_PARAMETER_END_DATE = OpenApiParameter(
    name="end_date",
    type=str,
    location=OpenApiParameter.QUERY,
    description="경기 일정 조회 종료일 (형식: YYYY-MM-DD)",
    required=False,
)

SWAGGER_GAMES_LIST = extend_schema(
    tags=SWAGGER_GAMES_TAGS,
    summary="경기 일정 목록 조회",
    description="지정된 기간 동안의 경기 일정을 조회합니다. "
    "시작일과 종료일을 지정하지 않으면 전체 경기 일정을 반환합니다.",
    parameters=[
        QUERY_PARAMETER_START_DATE,
        QUERY_PARAMETER_END_DATE,
    ],
    responses={200: GameSerializer(many=True)},
)
