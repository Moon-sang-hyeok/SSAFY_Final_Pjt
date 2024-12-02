# accounts/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import CustomUser  # CustomUser 모델을 임포트
from .serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from products.serializers import SavingProductsSerializer, DepositProductsSerializer

# 회원가입 뷰
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        full_name = request.data.get('fullname')  # 사용자 이름
        password = request.data.get('password')
        email = request.data.get('email')  # 이메일을 추가로 받기

        if not username or not full_name or not password:
            return Response({"detail": "username, fullname, and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자가 이미 존재하는지 확인
        if CustomUser.objects.filter(username=username).exists():  # CustomUser로 변경
            return Response({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(email=email).exists():  # 이메일 중복 체크
            return Response({"detail": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        # 사용자 생성
        user = CustomUser.objects.create_user(username=username, password=password, email=email)  # CustomUser로 변경
        user.full_name = full_name  # 사용자 이름을 full_name에 저장
        user.save()

        return Response({"message": "회원가입 성공", "id": user.id}, status=status.HTTP_201_CREATED)


# 로그인 뷰
class LoginView(APIView):
    def post(self, request):
        # 로그인에 필요한 데이터를 요청에서 가져옵니다.
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            
            # 사용자 인증
            user = authenticate(username=username, password=password)
            if user is not None:
                # 로그인 성공 시 JWT 토큰 발급
                refresh = RefreshToken.for_user(user)
                return Response({
                    'token': str(refresh.access_token),
                    "user_id": user.id,# 클라이언트에서 이 토큰만 받기 위해 수정
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 로그인 상태를 확인하는 뷰 (JWT 토큰 기반)
class UserStatusView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request):
        user = request.user
        return Response({
            "is_logged_in": True,
            "user": {
                "username": user.username,
                "full_name": user.full_name,  # 사용자 이름
                "email": user.email,
            }
        })
        

class UserFinancialProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # 사용자가 가입한 금융 상품
        saving_products = user.saving_products.all()
        deposit_products = user.deposit_products.all()
        
        # Serialize data
        saving_products_serializer = SavingProductsSerializer(saving_products, many=True)
        deposit_products_serializer = DepositProductsSerializer(deposit_products, many=True)

        return Response({
            "savings": saving_products_serializer.data,
            "deposits": deposit_products_serializer.data
        })
    

class CancelProductView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def delete(self, request, product_id):
        user = request.user  # 현재 인증된 사용자
        # 사용자에 해당하는 상품 찾기 (적금/예금 상품)
        saving_product = user.saving_products.filter(id=product_id).first()
        deposit_product = user.deposit_products.filter(id=product_id).first()

        if saving_product:
            # 적금 상품 삭제
            saving_product.delete()
            return Response({"detail": "적금 상품이 해지되었습니다."}, status=status.HTTP_204_NO_CONTENT)

        if deposit_product:
            # 예금 상품 삭제
            deposit_product.delete()
            return Response({"detail": "예금 상품이 해지되었습니다."}, status=status.HTTP_204_NO_CONTENT)

        # 상품을 찾을 수 없는 경우
        return Response({"detail": "상품을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)