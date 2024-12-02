# portfolio/serializers.py
from rest_framework import serializers
from .models import Portfolio

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ['id','user', 'product_name', 'bank', 'interest_rate']
        
