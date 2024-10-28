from drf_spectacular.utils import extend_schema, OpenApiParameter

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

SWAGGER_USERS_ME = extend_schema(
    tags=SWAGGER_USERS_TAGS,
    summary="내 정보 확인",
    description="내 정보를 확인 합니다.",
)
