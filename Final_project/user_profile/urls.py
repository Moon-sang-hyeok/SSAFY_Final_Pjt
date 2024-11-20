# user_profile/urls.py
from django.urls import path
from .views import user_info, financial_products, user_info_update

urlpatterns = [
    path('profile/', user_info, name='user_info'),  # 사용자 정보 조회
    path('profile/update/', user_info_update, name='user_info_update'),  # 사용자 정보 수정
    path('financial-products/', financial_products, name='financial_products'),  # 금융 상품 조회
]
