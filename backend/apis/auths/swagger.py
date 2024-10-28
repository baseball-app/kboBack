from drf_spectacular.utils import extend_schema, OpenApiParameter

SWAGGER_AUTHS_TAGS = ["AUTHS"]

QUERY_PARAMETER_CODE = OpenApiParameter(
    name="code",
    type=str,
    location=OpenApiParameter.QUERY,
    description="code",
    required=True,
)

QUERY_PARAMETER_STATE = OpenApiParameter(
    name="state",
    type=str,
    location=OpenApiParameter.QUERY,
    description="state",
    required=True,
)

SWAGGER_AUTHS_NAVER = extend_schema(
    tags=SWAGGER_AUTHS_TAGS,
    summary="네이버 소셜 로그인",
    description="네이버 아이디로 로그인",
    parameters=[QUERY_PARAMETER_CODE, QUERY_PARAMETER_STATE],
)

SWAGGER_AUTHS_KAKAO = extend_schema(
    tags=SWAGGER_AUTHS_TAGS,
    summary="카카오 소셜 로그인",
    description="카카오 아이디로 로그인",
    parameters=[QUERY_PARAMETER_CODE, QUERY_PARAMETER_STATE],
)
