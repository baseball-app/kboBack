from django.urls import path, include
from rest_framework import routers

from .views import TicketsViewSet

router = routers.DefaultRouter()
router.register("", TicketsViewSet, basename="ticket")

urlpatterns = [
    path("", include(router.urls)),
]
