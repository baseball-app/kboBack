from drf_spectacular.utils import extend_schema_view
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import NaverInputSerializer, KakaoInputSerializer
from .services import NaverAuthService, KakaoAuthService
from .swagger import SWAGGER_AUTHS_NAVER, SWAGGER_AUTHS_KAKAO


@extend_schema_view(
    naver=SWAGGER_AUTHS_NAVER,
    kakao=SWAGGER_AUTHS_KAKAO,
)
class AuthsViewSet(
    GenericViewSet
):
    @action(methods=["POST"], detail=False, permission_classes=[AllowAny])
    def naver(self, request):
        serializer = NaverInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        auth_service = NaverAuthService()
        user = auth_service.get_social_user(data=data)

        # token 정보를 내려주도록 수정 필요
        return Response()

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny])
    def kakao(self, request):
        serializer = KakaoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        auth_service = KakaoAuthService()
        user = auth_service.get_social_user(data=data)

        # token 정보를 내려주도록 수정 필요
        return Response()
