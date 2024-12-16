from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from rest_framework import serializers

SWAGGER_USERS_TAGS = ["USERS"]

QUERY_PARAMETER_EMAIL = OpenApiParameter(
    name="email",
    type=str,
    location=OpenApiParameter.QUERY,
    description="이메일",
    required=False,
)

QUERY_PARAMETER_PASSWORD = OpenApiParameter(
    name="password",
    type=str,
    location=OpenApiParameter.QUERY,
    description="비밀번호",
    required=False,
)

BODY_PARAMETER_FOR_FOLLOW = inline_serializer(
    name="follow",
    fields={
        "source_id": serializers.IntegerField(),
        "target_id": serializers.IntegerField(),
    },
)

BODY_PARAMETER_FOR_UNFOLLOW = inline_serializer(
    name="unfollow",
    fields={
        "source_id": serializers.IntegerField(),
        "target_id": serializers.IntegerField(),
    },
)

SWAGGER_USERS_ME = extend_schema(
    tags=SWAGGER_USERS_TAGS,
    summary="내 정보 확인",
    description="내 정보를 확인 합니다.",
)

SWAGGER_USERS_FOLLOW = extend_schema(
    tags=SWAGGER_USERS_TAGS,
    summary="친구 팔로우",
    description="친구를 팔로우 합니다.",
    request=BODY_PARAMETER_FOR_FOLLOW,
)

SWAGGER_USERS_UNFOLLOW = extend_schema(
    tags=SWAGGER_USERS_TAGS,
    summary="친구 언팔로우",
    description="친구를 언팔로우 합니다.",
    request=BODY_PARAMETER_FOR_UNFOLLOW,
)
