from django.contrib.admin import AdminSite
from django.contrib.auth import get_user_model
from django.template.response import TemplateResponse
from django.urls import path

from apps.admins.custom_forms import SecretKeyAdminAuthenticationForm
from apps.tickets.models import Ticket


class CustomAdminSite(AdminSite):
    site_header = "관리자 대시보드"
    site_title = "관리자 대시보드"
    index_title = "관리자 대시보드"
    login_form = SecretKeyAdminAuthenticationForm

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('', self.admin_view(self.dashboard_view), name="index"),
        ]
        return my_urls + urls[1:]

    def dashboard_view(self, request):
        User = get_user_model()
        user_count = User.objects.count()
        ticket_count = Ticket.objects.count()
        context = dict(
            self.each_context(request),
            user_count=user_count,
            ticket_count=ticket_count,
        )
        return TemplateResponse(request, "admin/custom_dashboard.html", context)


custom_admin_site = CustomAdminSite(name="custom_admin")
