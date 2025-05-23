from django.db import models


class AdminSecretKey(models.Model):
    key = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"비밀키 생성일: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
