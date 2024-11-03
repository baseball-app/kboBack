from django.urls import path, include
from rest_framework import routers

from .views import AlertsViewSet

router = routers.DefaultRouter()
router.register("", AlertsViewSet, basename="alert")

urlpatterns = [
    path("", include(router.urls)),
]
