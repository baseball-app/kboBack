from drf_spectacular.utils import extend_schema_view
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import UserSerializer
from .swagger import SWAGGER_USERS_ME


@extend_schema_view(
    me=SWAGGER_USERS_ME,
)
class UsersViewSet(GenericViewSet):

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
