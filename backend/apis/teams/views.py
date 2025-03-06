from rest_framework.viewsets import GenericViewSet

from base.mixins import SentryLoggingMixin


class TeamsViewSet(
    SentryLoggingMixin,
    GenericViewSet,
):
    pass
