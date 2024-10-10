from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'  # 모든 필드 포함, 필요에 따라 선택적인 필드만 지정 가능
