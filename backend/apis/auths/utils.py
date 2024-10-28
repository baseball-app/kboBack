from datetime import timedelta
from random import SystemRandom

from django.utils import timezone
from oauth2_provider.models import Application, AccessToken, RefreshToken

from conf import settings

UNICODE_ASCII_CHARACTER_SET = ('abcdefghijklmnopqrstuvwxyz'
                               'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                               '0123456789')


def issue_tokens(user):
    application = Application.objects.get(name='dev')
    scope = 'read write'
    expires_in = settings.DEFAULT_EXIRES_IN
    token_type = 'Bearer'

    # 토큰 만료 시점 생성
    expires = timezone.now() + timedelta(seconds=settings.DEFAULT_EXIRES_IN)

    # 엑세스 토큰 생성
    access_token = AccessToken.objects.create(
        user=user,
        application=application,
        token=generate_token(),
        expires=expires,
        scope=scope
    )

    # 리프레시 토큰 생성
    refresh_token = RefreshToken.objects.create(
        user=user,
        application=application,
        token=generate_token(),
        access_token=access_token
    )

    return {
        'access_token': access_token.token,
        'refresh_token': refresh_token.token,
        'scope': scope,
        'expires_in': expires_in,
        'token_type': token_type,
    }


def generate_token(length=30, chars=UNICODE_ASCII_CHARACTER_SET):
    rand = SystemRandom()
    return ''.join(rand.choice(chars) for x in range(length))
