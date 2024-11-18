from django.urls import path, include
from rest_framework import routers

from .views import NotificationsViewSet

router = routers.DefaultRouter()
router.register("", NotificationsViewSet, basename="notifications")

urlpatterns = [
    path("", include(router.urls)),
]
