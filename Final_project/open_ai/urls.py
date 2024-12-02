from django.urls import path
from .views import OPENAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/open_ai/', OPENAPIView.as_view(), name='openapi'),
    
]
