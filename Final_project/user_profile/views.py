# user_profile/views.py

from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User  # 사용자 모델 임포트
from .models import FinancialProduct
from .serializers import FinancialProductSerializer, UserSerializer

# 사용자 정보 조회
@api_view(['GET'])
def user_info(request):
    """
    로그인한 사용자 정보를 반환하는 API
    """
    if request.user.is_authenticated:
        # 사용자 정보 직렬화
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    else:
        return Response({"detail": "Unauthorized"}, status=401)

# 사용자 정보 수정
@api_view(['PATCH'])
def user_info_update(request):
    """
    로그인한 사용자의 정보를 수정하는 API
    """
    if request.user.is_authenticated:
        # 직렬화하여 데이터를 받음
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()  # 수정된 정보를 저장
            return Response({"message": "프로필이 성공적으로 업데이트되었습니다."})
        return Response(serializer.errors, status=400)
    else:
        return Response({"detail": "Unauthorized"}, status=401)

# 로그인한 사용자의 금융 상품 목록 조회
@api_view(['GET'])
def financial_products(request):
    """
    로그인한 사용자의 금융 상품 목록을 조회하는 API
    """
    if request.user.is_authenticated:
        products = FinancialProduct.objects.filter(user=request.user)
        serializer = FinancialProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"detail": "Unauthorized"}, status=401)
