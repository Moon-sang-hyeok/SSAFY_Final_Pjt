# urls.py

from django.urls import path
from .views import ExchangeRateView

urlpatterns = [
    path('api/exchange-rates/', ExchangeRateView.as_view(), name='exchange_rates'),
]
