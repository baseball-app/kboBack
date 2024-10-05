from django.urls import path
from .views import TicketCreateApi
app_name = "tickets"

urlpatterns=[
    path('create/', TicketCreateApi.as_view(), name = "ticket_create"),
]