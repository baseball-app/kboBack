from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apis.users.serializers import UserSerializer
from apis.users.swagger import SWAGGER_USERS_SIGN_UP, SWAGGER_USERS_ME


@extend_schema_view(
    sign_up=SWAGGER_USERS_SIGN_UP,
    me=SWAGGER_USERS_ME,
)
class UsersViewSet(GenericViewSet):
    @action(
        methods=["POST"],
        detail=False,
        url_path="sign-up",
        permission_classes=[AllowAny],
    )
    def sign_up(self, request):
        serializer = UserSerializer(request.user)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(
            status=status.HTTP_201_CREATED,
            data={"email": data.get("email"), "nickname": data.get("nickname")},
        )

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
