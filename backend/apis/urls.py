from django.urls import path, include

urlpatterns = [
    path("alerts/", include("apis.alerts.urls")),
    path("auths/", include("apis.auths.urls")),
    path("games/", include("apis.games.urls")),
    path("tickets/", include("apis.tickets.urls")),
    path("users/", include("apis.users.urls")),
    path("notifications/", include("apis.notifications.urls")),
]
