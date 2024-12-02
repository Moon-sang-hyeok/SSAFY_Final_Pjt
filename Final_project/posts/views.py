# posts/views.py

from rest_framework import viewsets, permissions
from rest_framework.exceptions import NotFound
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors to edit or delete their posts or comments.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True
        return obj.author == request.user

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.is_authenticated:
            # 인증된 사용자만 Post를 작성할 수 있도록 함
            serializer.save(author=user)
        else:
            # 인증되지 않은 사용자는 Post를 작성할 수 없음
            raise PermissionDenied("You must be logged in to create a post.")

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]  # 작성자만 수정/삭제 가능

    def perform_create(self, serializer):
        try:
            # 댓글을 작성하려는 게시글 찾기
            post = Post.objects.get(id=self.request.data['post'])
            serializer.save(author=self.request.user, post=post)
        except Post.DoesNotExist:
            raise NotFound('The specified post does not exist.')

