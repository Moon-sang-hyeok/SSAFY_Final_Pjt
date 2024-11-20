from django.db import models
from django.conf import settings  # settings 모듈을 import하여 AUTH_USER_MODEL을 사용

# 금융 상품 모델 예시
class FinancialProduct(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='financial_products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    joined_date = models.DateField()

    def __str__(self):
        return self.name
