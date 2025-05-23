from django.apps import apps
from django.contrib import admin

from .custom_site import custom_admin_site
from .mixins import ReadOnlyAdminMixin


class ReadOnlyAdmin(ReadOnlyAdminMixin, admin.ModelAdmin):
    pass


INCLUDE_MODELS = {}


def register_essential_models():
    for app_config in apps.get_app_configs():
        for model in app_config.get_models():
            if model in INCLUDE_MODELS:
                custom_admin_site.register(model, ReadOnlyAdmin)


register_essential_models()
