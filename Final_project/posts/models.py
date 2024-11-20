from django.conf import settings
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 수정된 부분
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title