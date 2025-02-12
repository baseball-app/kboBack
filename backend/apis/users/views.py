from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import (
    UserInfoSerializer,
    UserFollowSerializer,
    UserInvitationSerializer,
    UserFollowersSerializer,
    UserFollowingsSerializer,
    UserModifySerializer,
)
from .services import UserFollowService, UserInvitationService, UserLeaveService, UserModifyService
from .swagger import (
    SWAGGER_USERS_ME,
    SWAGGER_USERS_FOLLOW,
    SWAGGER_USERS_UNFOLLOW,
    SWAGGER_USERS_LEAVE,
    SWAGGER_USERS_INVITATION_CODE,
    SWAGGER_USERS_APPLY_INVITATION,
    SWAGGER_USERS_FOLLOWERS,
    SWAGGER_USERS_FOLLOWINGS,
    SWAGGER_USERS_MODIFY,
)


@extend_schema_view(
    me=SWAGGER_USERS_ME,
    modify=SWAGGER_USERS_MODIFY,
    leave=SWAGGER_USERS_LEAVE,
    follow=SWAGGER_USERS_FOLLOW,
    unfollow=SWAGGER_USERS_UNFOLLOW,
    followers=SWAGGER_USERS_FOLLOWERS,
    followings=SWAGGER_USERS_FOLLOWINGS,
    invitation_code=SWAGGER_USERS_INVITATION_CODE,
    apply_invitation=SWAGGER_USERS_APPLY_INVITATION,
)
class UsersViewSet(GenericViewSet):
    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserInfoSerializer(request.user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def modify(self, request):
        serializer = UserModifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        service = UserModifyService()
        service.modify(request.user, validated_data)

        return Response(status=status.HTTP_200_OK, data=validated_data)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def leave(self, request):
        service = UserLeaveService()
        service.leave(request.user.id)

        return Response(status=status.HTTP_200_OK)

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

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def followers(self, request):
        serializer = UserFollowersSerializer(instance=request.user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def followings(self, request):
        serializer = UserFollowingsSerializer(instance=request.user)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    @action(methods=["GET"], url_path="invitation-code", detail=False, permission_classes=[IsAuthenticated])
    def invitation_code(self, request):
        service = UserInvitationService()
        code = service.generate_invite_code(request.user.id)

        serializer = UserInvitationSerializer(data={"code": code})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        return Response(status=status.HTTP_200_OK, data=data)

    @action(methods=["POST"], url_path="apply-invitation", detail=False, permission_classes=[IsAuthenticated])
    def apply_invitation(self, request):
        serializer = UserInvitationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        service = UserInvitationService()
        user_id = service.decode_invite_code(data.get("code"))

        return Response(status=status.HTTP_200_OK, data={"user_id": user_id})
