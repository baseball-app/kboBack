from django.urls import path, include
from rest_framework import routers

from .views import TeamsViewSet

router = routers.DefaultRouter()
router.register("", TeamsViewSet, basename="team")

urlpatterns = [
    path("", include(router.urls)),
]
