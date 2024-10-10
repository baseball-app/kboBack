from rest_framework import viewsets, permissions
from .models import Notification
from rest_framework.response import Response

from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer  # 필요에 따라 Serializer 정의

    permission_classes = [permissions.IsAuthenticated] # 인증된 사용자만 접근 가능하도록 설정

    def list(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)

    # ... (추가 API 엔드포인트 정의 가능) ...
