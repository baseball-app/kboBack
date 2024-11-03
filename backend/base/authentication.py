from django.conf import settings
from django.contrib.auth import get_user_model
from oauth2_provider.models import AccessToken
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class CustomHeaderAuthentication(BaseAuthentication):
    def authenticate(self, request):
        access_token = request.META.get(settings.CUSTOM_HEADER_NAME)
        if not access_token:
            return None

        token = AccessToken.objects.filter(token=access_token).last()
        if not token or not token.is_valid():
            return None

        user = token.user
        if not user:
            raise AuthenticationFailed('Invalid token')

        return user, None

    # def get_user_from_token(self, token):
    #     access_token = AccessToken.objects.filter(token=token).last()
    #     if not access_token or not access_token.is_valid():
    #         return None
    #
    #     return access_token.user
