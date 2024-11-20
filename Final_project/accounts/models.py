# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)  # 이메일 필드 추가 (고유값으로 설정)

    def __str__(self):
        return self.username
