from django.urls import path, include
from rest_framework import routers

from .views import UploadsViewSet

router = routers.DefaultRouter()
router.register("", UploadsViewSet, basename="uploads")

urlpatterns = [
    path("", include(router.urls)),
]
