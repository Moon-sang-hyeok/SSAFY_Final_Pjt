# portfolio/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('portfolio/', views.create_portfolio, name='create_portfolio'),  # 포트폴리오 생성
    path('portfolio/list/', views.get_portfolio, name='get_portfolio'),  # 포트폴리오 조회
    path('portfolio/list/<int:pk>/', views.delete_portfolio, name='delete_portfolio'),  # 포트폴리오 삭제
]
