from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer, OpenApiExample
from rest_framework import serializers

SWAGGER_USERS_TAGS = ["users"]

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

BODY_PARAMETER_FOR_MODIFY = inline_serializer(
    name="modify",
    fields={
        "nickname": serializers.CharField(),
        "my_team": serializers.IntegerField(),
        "profile_image": serializers.CharField(),
    },
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

BODY_PARAMETER_FOR_APPLY_INVITATION = inline_serializer(
    name="apply_invitation",
    fields={
        "code": serializers.CharField(),
    },
)

SWAGGER_USERS_ME = extend_schema(
    tags=SWAGGER_USERS_TAGS,
    summary="내 정보 확인",
    description="내 정보를 확인 합니다.",
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            name="Success Example",
            value={
                "nickname": "nickname",
                "predict_ratio": 1,
                "my_team": {
                    "id": 3,
                    "name": "LG 트윈스",
                    "logo_url": "https://image.com/"
                },
                "followers": 20,
                "followings": 32
            },
            response_only=True
        )
    ],
)

SWAGGER_USERS_MODIFY = extend_schema(
    tags=SWAGGER_USERS_TAGS,
    summary="회원 정보 수정",
    description="회원 정보를 수정 합니다.",
    request=BODY_PARAMETER_FOR_MODIFY,
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            name="Success Example",
            value={
                "nickname": "nickname",
                "my_team": 1,
                "profile_image": "profile_image"
            },
            response_only=True
        )
    ],
)

SWAGGER_USERS_LEAVE = extend_schema(
    tags=SWAGGER_USERS_TAGS,
    summary="회원 탈퇴",
    description="회원에서 탈퇴 합니다.",
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

SWAGGER_USERS_FOLLOWERS = extend_schema(
    tags=SWAGGER_USERS_TAGS,
    summary="팔로워 조회",
    description="팔로워를 조회 합니다.",
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            name="Success Example",
            value={"followers": [{"nickname": "user1", "profile_image": ""}]},
            response_only=True
        )
    ],
)

SWAGGER_USERS_FOLLOWINGS = extend_schema(
    tags=SWAGGER_USERS_TAGS,
    summary="팔로잉 조회",
    description="팔로잉 한 친구를 조회 합니다.",
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            name="Success Example",
            value={"followings": [{"nickname": "user1", "profile_image": ""}]},
            response_only=True
        )
    ],
)

SWAGGER_USERS_INVITATION_CODE = extend_schema(
    tags=SWAGGER_USERS_TAGS,
    summary="친구 초대 코드 발급",
    description="친구 초대를 위한 초대 코드 발급",
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            name="Success Example",
            value={"code": "abcdefghijklmnopqrstuvwxyz="},
            response_only=True
        )
    ],
)

SWAGGER_USERS_APPLY_INVITATION = extend_schema(
    tags=SWAGGER_USERS_TAGS,
    summary="친구 초대 코드 수락",
    description="전달 받은 친구 코드로 친구 수락",
    request=BODY_PARAMETER_FOR_APPLY_INVITATION,
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            name="Success Example",
            value={"user_id": "1"},
            response_only=True
        )
    ],
)
