from rest_framework.serializers import ModelSerializer

from apps.notifications.models import Notification
from apps.users.models import User


class NotificationUserInfoSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "nickname",
            "profile_image",
        ]


class NotificationSerializer(ModelSerializer):
    user_info = NotificationUserInfoSerializer(read_only=True, source="feedback_user")

    class Meta:
        model = Notification
        fields = [
            "id",
            "user_info",
            "ticket",
            "type",
            "is_read",
            "created_at",
            "updated_at",
        ]
