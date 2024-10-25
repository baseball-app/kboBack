from django.urls import path, include
from rest_framework import routers

from .views import AuthsViewSet

router = routers.DefaultRouter()
router.register('', AuthsViewSet, basename="auths")

urlpatterns = [
    path('', include(router.urls)),
]
