from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apis.teams.serializers import TeamsSerializer, UserTeamInputSerializer
from apps.teams.models import Team, UserTeam


class TeamsViewSet(
    GenericViewSet,
):

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def my(self, request):
        user = request.user
        team_id = UserTeam.objects.get(user=user).team_id
        serializer = TeamsSerializer(Team.objects.get(id=team_id))
        return Response(serializer.data)

    @action(methods=["POST"], detail=False, permission_classes=[IsAuthenticated])
    def change(self, request):
        user = request.user
        input_serializer = UserTeamInputSerializer(UserTeam.objects.get(user=user), data=request.data)
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()
        team_id = UserTeam.objects.get(user=user).team_id
        serializer = TeamsSerializer(Team.objects.get(id=team_id))
        return Response(serializer.data)
