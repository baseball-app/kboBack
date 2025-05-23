import secrets

import requests
from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.admins.models import AdminSecretKey
from conf.settings.base import DISCORD_WEBHOOK_URL, DISCORD_SECRET_KEY_URL

User = get_user_model()


@shared_task
def generate_admin_secret_key():
    new_key = secrets.token_urlsafe(12)
    AdminSecretKey.objects.create(key=new_key)
    now = timezone.localtime().strftime('%Y년 %m월 %d일 %H:%M')

    message = {
        "content": f"🔑 {now} 의 관리자 비밀키: {new_key}"
    }

    try:
        response = requests.post(DISCORD_SECRET_KEY_URL, json=message)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"디스코드 전송 실패: {e}")
