from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FinancialProduct

# 사용자 정보 직렬화
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']  # 필요한 필드를 추가

# 금융 상품 직렬화
class FinancialProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialProduct
        fields = ['id', 'name', 'interest_rate', 'joined_date', 'user']
