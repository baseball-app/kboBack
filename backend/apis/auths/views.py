from django.contrib.auth import get_user_model, login
from django.utils import timezone
from drf_spectacular.utils import extend_schema_view
from oauth2_provider.models import AccessToken
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import NaverInputSerializer, KakaoInputSerializer
from .services import NaverAuthService, KakaoAuthService
from .swagger import SWAGGER_AUTHS_NAVER, SWAGGER_AUTHS_KAKAO
from .utils import issue_tokens
from ..exceptions import ApiValidationError

User = get_user_model()


@extend_schema_view(
    naver=SWAGGER_AUTHS_NAVER,
    kakao=SWAGGER_AUTHS_KAKAO,
)
class AuthsViewSet(GenericViewSet):
    @action(methods=["POST"], url_path='token-test', detail=False, permission_classes=[AllowAny])
    def token_test(self, request):
        user = User.objects.filter(id=int(request.data.get('user_id'))).first()
        return Response(issue_tokens(user), status=status.HTTP_200_OK)

    @action(methods=["POST"], url_path='naver/register', detail=False, permission_classes=[AllowAny])
    def naver_register(self, request):
        serializer = NaverInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        auth_service = NaverAuthService()

        if not auth_service.get_social_user(data=data):
            raise ApiValidationError('User is already existed.')

        # 유저 추가 로직 추가
        user = User.objects.create(social_id=data['id'])

        return Response(issue_tokens(user), status=status.HTTP_200_OK)

    @action(methods=["POST"], url_path='naver/token', detail=False, permission_classes=[AllowAny])
    def naver_token(self, request):
        serializer = NaverInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        auth_service = NaverAuthService()
        user = auth_service.get_social_user(data=data)

        return Response(issue_tokens(user), status=status.HTTP_200_OK)

    @action(methods=["POST"], url_path='naver/login', detail=False, permission_classes=[AllowAny])
    def naver_login(self, request):
        access_token_str = request.data.get('access_token')
        if not access_token_str:
            raise ApiValidationError('Access token is required.')

        try:
            access_token = AccessToken.objects.get(token=access_token_str, expires__gt=timezone.now())
            user = access_token.user
            login(request, user)
        except AccessToken.DoesNotExist:
            return ApiValidationError('Access token is not valid.')

        return Response(status=status.HTTP_200_OK)

    @action(methods=["POST"], url_path='kakao/register', detail=False, permission_classes=[AllowAny])
    def kakao_register(self, request):
        serializer = KakaoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        auth_service = KakaoAuthService()

        if not auth_service.get_social_user(data=data):
            raise ApiValidationError('User is already existed.')

        # 유저 추가 로직 추가
        user = User.objects.create(social_id=data['id'])

        return Response(issue_tokens(user), status=status.HTTP_200_OK)

    @action(methods=["POST"], url_path='kakao/token', detail=False, permission_classes=[AllowAny])
    def kakao_token(self, request):
        serializer = KakaoInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        auth_service = KakaoAuthService()
        user = auth_service.get_social_user(data=data)

        return Response(issue_tokens(user), status=status.HTTP_200_OK)

    @action(methods=["POST"], url_path='kakao/login', detail=False, permission_classes=[AllowAny])
    def kakao_login(self, request):
        access_token_str = request.data.get('access_token')
        if not access_token_str:
            raise ApiValidationError('Access token is required.')

        try:
            access_token = AccessToken.objects.get(token=access_token_str, expires__gt=timezone.now())
            user = access_token.user
            login(request, user)
        except AccessToken.DoesNotExist:
            return ApiValidationError('Access token is not valid.')

        return Response(status=status.HTTP_200_OK)
