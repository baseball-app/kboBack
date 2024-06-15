from django.urls import path
from .views import SignUpApi

app_name = "users"

urlpatterns=[
    path('signup/', SignUpApi.as_view(), name = "user_signup")
]