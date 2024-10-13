from django.urls import path, include
from rest_framework import routers

from apis.games.views import GamesViewSet

router = routers.DefaultRouter()
router.register('', GamesViewSet, basename="game")

urlpatterns = [
    path('', include(router.urls)),
]
