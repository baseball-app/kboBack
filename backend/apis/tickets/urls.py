from django.urls import path, include
from rest_framework import routers

from apis.tickets.views import TicketsViewSet

router = routers.DefaultRouter()
router.register("", TicketsViewSet, basename="ticket")

urlpatterns = [
    path("", include(router.urls)),
]
