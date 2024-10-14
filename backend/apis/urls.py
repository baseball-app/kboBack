from django.urls import path, include

urlpatterns = [
    path('alerts/', include('apis.alerts.urls')),
    path('games/', include('apis.games.urls')),
    path('tickets/', include('apis.tickets.urls')),
    path('users/', include('apis.users.urls')),
]
