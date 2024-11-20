# posts/urls.py
from django.urls import path
from .views import PostCreateView, PostListView

urlpatterns = [
    path('api/posts/', PostListView.as_view(), name='post-list'),  # 게시글 목록 조회
    path('api/posts/create/', PostCreateView.as_view(), name='post-create'),  # 게시글 작성
]
