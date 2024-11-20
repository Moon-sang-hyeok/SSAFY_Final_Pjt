from django.urls import path
from .views import NearbyBanksView

urlpatterns = [
    path('nearby-banks/', NearbyBanksView.as_view(), name='nearby-banks'),
]
