from django.urls import path, include
from rest_framework import routers

from .views import UsersViewSet

router = routers.DefaultRouter()
router.register("", UsersViewSet, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
