from rest_framework import serializers
from django.contrib.auth.models import User
from .models import FinancialProduct
from accounts.models import CustomUser  # CustomUser 모델을 임포트
# 사용자 정보 직렬화
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'full_name', 'email']  # 필요한 필드를 추가

# 금융 상품 직렬화
class FinancialProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialProduct
        fields = ['id', 'name', 'interest_rate', 'joined_date', 'user']
