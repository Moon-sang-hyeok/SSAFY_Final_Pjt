# posts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def post(self, request, *args, **kwargs):
        # 로그인된 사용자만 사용
        if not request.user.is_authenticated:
            return Response({"error": "사용자가 인증되지 않았습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        # 로그인한 사용자의 ID를 author 필드에 할당
        data = request.data
        data['author'] = request.user.id  # request.user.id는 로그인한 사용자의 id

        # Serializer 인스턴스를 생성하고 유효성 검사
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            try:
                post = serializer.save()  # 새 게시글 생성
                return Response(PostSerializer(post).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                # 예외가 발생한 경우
                return Response({"error": f"게시글 저장 중 오류 발생: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # 유효성 검사 실패 시 오류 반환
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
