from datetime import datetime

from drf_spectacular.utils import extend_schema_view
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apis.games.serializers import GameSerializer
from apis.games.swagger import SWAGGER_GAMES_LIST
from apps.games.models import Game


@extend_schema_view(
    list=SWAGGER_GAMES_LIST,
)
class GamesViewSet(
    ListModelMixin,
    GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    serializer_class = GameSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Game.objects.all()

        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)

        if start_date and end_date:
            try:
                start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
                end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
                queryset = queryset.filter(game_date__date__gte=start_datetime, game_date__date__lte=end_datetime)
            except ValueError:
                return Game.objects.none()

        return queryset.select_related("team_home", "team_away", "ballpark", "ballpark__team")
