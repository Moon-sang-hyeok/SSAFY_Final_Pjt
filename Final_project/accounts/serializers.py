# accounts/serializers.py
from rest_framework import serializers
from accounts.models import CustomUser

# UserSerializer 정의 (오타 없이)
class UserSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

# RegisterSerializer 정의 (회원가입을 위한 serializer)
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(style={'input_type': 'password'})
