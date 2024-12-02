from django.contrib.auth.models import AbstractUser
from django.db import models
from products.models import SavingProducts, DepositProducts  # 금융상품 모델 import

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    
    # 사용자가 가입한 금융상품 목록
    saving_products = models.ManyToManyField(SavingProducts, blank=True, related_name='subscribed_users')
    deposit_products = models.ManyToManyField(DepositProducts, blank=True, related_name='subscribed_users')

    def __str__(self):
        return self.username