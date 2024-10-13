from django.urls import path, include
from rest_framework import routers

from .views import UserSignUpApi, UpdateMyTeamApi, ChangePasswordView, UserLoginApi, UsersViewSet

router = routers.DefaultRouter()
router.register('', UsersViewSet, basename="user")

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', UserSignUpApi.as_view(), name="user_signup"),
    path('myteam/<int:pk>/', UpdateMyTeamApi.as_view(), name="update_myteam"),
    path('<int:pk>/password/', ChangePasswordView.as_view(), name='change_password'),
    path('login/', UserLoginApi.as_view(), name='login'),
]
