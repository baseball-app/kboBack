from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('users/', include('apis.users.urls')),
    path('tickets/', include('apis.tickets.urls')),
]
