from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers

SWAGGER_AUTHS_TAGS = ["auths"]

BODY_PARAMETER_FOR_TOKEN = inline_serializer(
    name="code",
    fields={
        "native": serializers.BooleanField(),
        "id_token": serializers.CharField(),
        "code": serializers.CharField(),
        "state": serializers.CharField(),
    },
)

BODY_PARAMETER_REFRESH_TOKEN = inline_serializer(
    name="refresh_token",
    fields={
        "refresh_token": serializers.CharField(),
    },
    required=True,
)

SWAGGER_NAVER = extend_schema(
    tags=SWAGGER_AUTHS_TAGS,
    summary="네이버 소셜 로그인하여 회원가입/로그인",
    description="네이버 아이디로 로그인하여 회원가입/로그인",
    request=BODY_PARAMETER_FOR_TOKEN,
)

SWAGGER_KAKAO = extend_schema(
    tags=SWAGGER_AUTHS_TAGS,
    summary="카카오 소셜 로그인하여 회원가입/로그인",
    description="카카오 아이디로 로그인하여 회원가입/로그인",
    request=BODY_PARAMETER_FOR_TOKEN,
)

SWAGGER_APPLE = extend_schema(
    tags=SWAGGER_AUTHS_TAGS,
    summary="애플 소셜 로그인하여 회원가입/로그인",
    description="애플 아이디로 로그인하여 회원가입/로그인",
    request=BODY_PARAMETER_FOR_TOKEN,
)

SWAGGER_TOKEN_REFRESH = extend_schema(
    tags=SWAGGER_AUTHS_TAGS,
    summary="토큰 새로고침",
    description="토큰 새로고침",
    request=BODY_PARAMETER_REFRESH_TOKEN,
)

SWAGGER_TOKEN_REVOKE = extend_schema(
    tags=SWAGGER_AUTHS_TAGS,
    summary="토큰 무효화(로그아웃)",
    description="토큰 무효화(로그아웃)",
    parameters=[],
)
