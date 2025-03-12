from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

SWAGGER_TEAMS_TAGS = ["TEAMS"]

# 팀 목록 응답을 위한 시리얼라이저
TEAMS_LIST_RESPONSE = inline_serializer(
    name="TeamsList",
    fields={
        "id": serializers.IntegerField(),
        "name": serializers.CharField(),
        "logo_url": serializers.URLField(),
    },
    many=True,
)

SWAGGER_TEAMS_LIST = extend_schema(
    tags=SWAGGER_TEAMS_TAGS,
    summary="팀 목록 조회",
    description="KBO 리그의 전체 팀 목록을 조회합니다.",
    responses={200: TEAMS_LIST_RESPONSE},
)
