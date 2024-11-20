# accounts/views.py

# accounts/views.py
from rest_framework.permissions import AllowAny
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import CustomUser  # CustomUser 모델을 임포트
from django.contrib.auth import authenticate
from .serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListCreateAPIView

class RegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        fullname = request.data.get('fullname')  # 사용자 이름
        password = request.data.get('password')
        email = request.data.get('email')  # 이메일

        if not username or not fullname or not password:
            return Response({"detail": "username, fullname, email, and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # 사용자가 이미 존재하는지 확인
        if CustomUser.objects.filter(username=username).exists():  # CustomUser로 변경
            return Response({"detail": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        if CustomUser.objects.filter(email=email).exists():
            return Response({"detail": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
        # 사용자 생성
        user = CustomUser.objects.create_user(username=username, password=password,email=email,)  # CustomUser로 변경
        user.full_name = fullname  # 사용자 이름을 full_name에 저장
        user.save()

        return Response({"message": "회원가입 성공", "id": user.id}, status=status.HTTP_201_CREATED)


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
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            # 사용자 인증
            user = User.objects.get(username=username)
            if user.check_password(password):  # 비밀번호 확인
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        

