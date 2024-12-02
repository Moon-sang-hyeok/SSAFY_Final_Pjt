# serializers.py
from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)  # 작성자의 ID 추가
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'author', 'author_id']

class PostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    author_id = serializers.IntegerField(source='author.id', read_only=True)  # 작성자의 ID 추가
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'author', 'comments', 'author_id']
