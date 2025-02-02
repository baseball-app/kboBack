from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample

SWAGGER_UPLOADS_TAGS = ["uploads"]

SWAGGER_UPLOADS_PROFILE = extend_schema(
    tags=SWAGGER_UPLOADS_TAGS,
    summary="프로필 이미지 업로드",
    description="프로필 이미지를 업로드 합니다.",
    request={"multipart/form-data": {"type": "object", "properties": {"file": {"type": "string", "format": "binary"}}}},
    responses={200: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            name="Success Example",
            value={
                "file_key": "123/file_key",
            },
            response_only=True,
        )
    ],
)
