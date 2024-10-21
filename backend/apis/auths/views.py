from drf_spectacular.utils import extend_schema_view
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from apis.auths.serializers import NaverInputSerializer
from apis.auths.services import NaverAuthService
from apis.auths.swagger import SWAGGER_AUTHS_NAVER, SWAGGER_AUTHS_KAKAO


@extend_schema_view(
    naver=SWAGGER_AUTHS_NAVER,
    kakao=SWAGGER_AUTHS_KAKAO,
)
class AuthsViewSet(
    GenericViewSet
):
    @action(methods=["POST"], detail=False, permission_classes=[AllowAny])
    def naver(self, request):
        serializer = NaverInputSerializer(request)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        auth_service = NaverAuthService()
        user = auth_service.get_social_user(data=data)

        return user
