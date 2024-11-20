# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from rest_framework.authtoken.models import Token


# CustomUser 모델을 관리하기 위한 관리자 설정
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'full_name', 'email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'full_name']
    ordering = ['username']

    # 비밀번호 변경을 위한 필드 설정
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('full_name',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('full_name',)}),
    )

# CustomUser 모델을 관리자에 등록
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Token)
