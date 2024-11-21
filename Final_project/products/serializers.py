# accounts/serializers.py

# UserSerializer 정의 (오타 없이)

from rest_framework import serializers
from .models import SavingProducts, DepositProducts

class SavingProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields = '__all__'


class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'