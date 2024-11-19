from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # 기본적인 username, password 외에도 full_name 필드를 추가합니다.
    full_name = models.CharField(max_length=255, blank=True, null=True)
    
    # 추가적인 필드를 더 추가할 수 있습니다.
    # 예: 이메일, 프로필 이미지, 전화번호 등
    
    def __str__(self):
        return self.username
