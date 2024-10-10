from django.db import models

# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # 알림을 받는 사용자
    friend = models.ForeignKey('User', related_name='notifications_sent', on_delete=models.CASCADE) # 게시물을 올린 친구
    post = models.ForeignKey('Post', on_delete=models.CASCADE)  # 관련 게시물

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False) # 알림 확인 여부

    def __str__(self):
        return f"{self.friend.nickname} 올린 새 게시물 알림"
