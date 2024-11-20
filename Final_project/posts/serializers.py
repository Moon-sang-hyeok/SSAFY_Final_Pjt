# posts/serializers.py
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.full_name', read_only=True)  # 사용자 이름을 가져옵니다.

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at']
