from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from base.mixins import SentryLoggingMixin
from .serializers import KakaoInputSerializer, NaverInputSerializer, TokenRefreshSerializer, AppleInputSerializer
from .services import NaverAuthService, KakaoAuthService, AppleAuthService
from .swagger import SWAGGER_TOKEN_REFRESH, SWAGGER_TOKEN_REVOKE, SWAGGER_NAVER, SWAGGER_KAKAO, SWAGGER_APPLE
from .utils import issue_tokens, reissue_tokens, revoke_tokens
from ..exceptions import ApiValidationError

User = get_user_model()


@extend_schema_view(
    naver=SWAGGER_NAVER,
    kakao=SWAGGER_KAKAO,
    apple=SWAGGER_APPLE,
    token_refresh=SWAGGER_TOKEN_REFRESH,
    token_revoke=SWAGGER_TOKEN_REVOKE,
    token_test=extend_schema(exclude=True),
    login_test=extend_schema(exclude=True),
)
class AuthsViewSet(SentryLoggingMixin, GenericViewSet):
    @action(methods=["POST"], url_path="token-test", detail=False, permission_classes=[AllowAny])
    def token_test(self, request):
        user = User.objects.filter(id=int(request.data.get("user_id"))).first()
        return Response(issue_tokens(user), status=status.HTTP_200_OK)

    @action(methods=["GET"], url_path="login-test", detail=False, permission_classes=[IsAuthenticated])
    def login_test(self, request):
        return Response({"message": "success"}, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny])
    def naver(self, request):
        serializer = NaverInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        auth_service = NaverAuthService()
        social_user_info = auth_service.get_social_user(data=data)
        if not social_user_info:
            raise ApiValidationError("Token is not valid")

        user, is_new_user = auth_service.auth_or_register(social_user_info)
        if not user:
            raise ApiValidationError("User is not valid")

        return Response({"is_new_user": is_new_user, **issue_tokens(user)}, status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny])
    def kakao(self, request):
        try:
            serializer = KakaoInputSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data

            auth_service = KakaoAuthService()
            social_user_info = auth_service.get_social_user(data=data)
            if not social_user_info:
                raise ApiValidationError("Token is not valid")

            user, is_new_user = auth_service.auth_or_register(social_user_info)
            if not user:
                raise ApiValidationError("User is not valid")

            return Response({"is_new_user": is_new_user, **issue_tokens(user)}, status=status.HTTP_200_OK)
        except ApiValidationError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "Internal Server Error", "error": str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=["POST"], detail=False, permission_classes=[AllowAny])
    def apple(self, request):
        serializer = AppleInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        auth_service = AppleAuthService()
        social_user_info = auth_service.get_social_user(data=data)
        if not social_user_info:
            raise ApiValidationError("Token is not valid")

        user, is_new_user = auth_service.auth_or_register(social_user_info)
        if not user:
            raise ApiValidationError("User is not valid")

        return Response({"is_new_user": is_new_user, **issue_tokens(user)}, status=status.HTTP_200_OK)

    @action(methods=["POST"], url_path="token/refresh", detail=False, permission_classes=[IsAuthenticated])
    def token_refresh(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        reissued_token = reissue_tokens(request.user, data.get("refresh_token"))
        if not reissued_token:
            raise ApiValidationError("Invalid token")

        return Response(reissued_token, status=status.HTTP_200_OK)

    @action(methods=["POST"], url_path="token/revoke", detail=False, permission_classes=[IsAuthenticated])
    def token_revoke(self, request):
        user = request.user
        revoke_tokens(user)

        return Response(status=status.HTTP_200_OK)
