from django.urls import path
from .views import RegisterView, LoginView, UserStatusView,UserFinancialProductsView,CancelProductView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('status/', UserStatusView.as_view(), name='user-status'),
    path('financial-products/', UserFinancialProductsView.as_view(), name='financial-products'),
    path('financial-products/<int:product_id>/cancel/', CancelProductView.as_view(), name='cancel-product'),
]
