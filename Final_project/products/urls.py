"""
URL configuration for Final_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import SavingProductsView,SavingDetailView,DepositProductsView,DepositDetailView,JoinSavingProductView, JoinDepositProductView, CombinedProductView


urlpatterns = [    
    path('api/savings-comparison/', SavingProductsView.as_view(), name='save-savings'),
    path('api/savings-comparison/<int:product_id>/', SavingDetailView.as_view(), name='saving-detail'),
    path('api/deposits-comparison/', DepositProductsView.as_view(), name='save-deposits'),
    path('api/deposits-comparison/<int:product_id>/', DepositDetailView.as_view(), name='deposit-detail'),
    path('api/savings/join/<int:product_id>/', JoinSavingProductView.as_view(), name='join-saving-product'),
    path('api/deposits/join/<int:product_id>/', JoinDepositProductView.as_view(), name='join-deposit-product'),  
    path('api/products/', CombinedProductView.as_view(), name='combined_products'),
]
