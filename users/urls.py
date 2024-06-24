from django.urls import path
from .views import UserSignUpApi, UpdateMyTeamApi, ChangePasswordView, UserLoginApi

app_name = "users"

urlpatterns=[
    path('signup/', UserSignUpApi.as_view(), name = "user_signup"),
    path('myteam/<int:pk>/', UpdateMyTeamApi.as_view(), name="update_myteam"),
    path('<int:pk>/password/', ChangePasswordView.as_view(), name='change_password'),
    path('login/', UserLoginApi.as_view(), name = 'login'),
]