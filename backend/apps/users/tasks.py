from django.utils import timezone

import requests
from celery import shared_task
from django.contrib.auth import get_user_model

from apps.tickets.models import Ticket
from conf.settings.base import DISCORD_WEBHOOK_URL

User = get_user_model()


@shared_task
def send_user_count_to_discord():
    current_user_count = User.objects.count()
    current_ticket_count = Ticket.objects.count()
    now = timezone.localtime().strftime('%Y년 %m월 %d일 %H:%M')
    message = {
        "content": f"📊 {now} 기준 유저 수: {current_user_count} 명 / 현재 티켓 수: {current_ticket_count} 개"
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=message)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"디스코드 전송 실패: {e}")
