from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import UserInfoSerializer, UserFollowSerializer
from .services import UserFollowService
from .swagger import SWAGGER_USERS_ME, SWAGGER_USERS_FOLLOW, SWAGGER_USERS_UNFOLLOW


@extend_schema_view(
    me=SWAGGER_USERS_ME,
    follow=SWAGGER_USERS_FOLLOW,
    unfollow=SWAGGER_USERS_UNFOLLOW,
)
class UsersViewSet(GenericViewSet):

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserInfoSerializer(request.user)
        return Response(serializer.data)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def follow(self, request):
        serializer = UserFollowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service = UserFollowService()
        service.make_relation(data.get("source_id"), data.get("target_id"))

        return Response(status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def unfollow(self, request):
        serializer = UserFollowSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service = UserFollowService()
        service.release_relation(data.get("source_id"), data.get("target_id"))

        return Response(status=status.HTTP_200_OK)
