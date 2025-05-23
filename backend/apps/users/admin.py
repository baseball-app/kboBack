from django.contrib import admin

from apps.admins.custom_site import custom_admin_site
from apps.admins.mixins import ReadOnlyAdminMixin
from . import models


@admin.register(models.User)
class User(admin.ModelAdmin):
    pass


@admin.register(models.Friendship)
class Friendship(admin.ModelAdmin):
    pass


@admin.register(models.UserInquiry, site=custom_admin_site)
class CustomUserInquiryAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    readonly_fields = ("created_at", "created_user")

    fieldsets = (
        ("문의 내용", {
            "fields": ("email", "title", "content"),
        }),
        ("메타 정보", {
            "fields": ("created_at", "created_user"),
        }),
    )

    list_display = ("email", "title", "created_at")
    search_fields = ("email", "title")
    ordering = ("-created_at",)
