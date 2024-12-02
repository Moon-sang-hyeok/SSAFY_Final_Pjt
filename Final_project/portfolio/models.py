# portfolio/models.py
from django.db import models
from django.conf import settings  # CustomUser를 사용하기 위해 settings를 임포트

class Portfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="portfolios")  # CustomUser 모델 사용
    product_name = models.CharField(max_length=255)  # 추천된 상품명
    bank = models.CharField(max_length=255)  # 추천된 은행명
    interest_rate = models.CharField(max_length=50)  # 이자율 (예: "3-5%" 또는 "3%")

    def __str__(self):
        return f"{self.product_name} - {self.bank} - {self.interest_rate}"
