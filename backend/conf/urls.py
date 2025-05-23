from django.contrib.auth.decorators import login_required
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from apps.admins.custom_site import custom_admin_site

urlpatterns = [
    path("kboapp-admin/", custom_admin_site.urls),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", login_required(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),
    path("", include("apis.urls")),
]
