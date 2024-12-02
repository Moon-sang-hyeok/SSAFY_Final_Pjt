# models.py

from django.db import models

class ExchangeRate(models.Model):
    # 기준 통화는 원화(KRW)로 설정하고 다른 통화들과의 환율을 저장
    currency = models.CharField(max_length=10)  # 통화명 (예: USD, EUR, JPY)
    rate = models.DecimalField(max_digits=15, decimal_places=4)  # 해당 통화와 원화의 환율 (예: 1200.5)
    last_updated = models.DateTimeField(auto_now=True)  # 마지막 업데이트 시간

    class Meta:
        unique_together = ('currency',)  # 동일 통화에 대해 중복된 데이터 저장 방지

    def __str__(self):
        return f'{self.currency} - {self.rate}'
