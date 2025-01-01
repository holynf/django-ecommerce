from rest_framework import serializers
from .models import Basket, BasketItem

class BasketItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasketItem
        fields = ['id', 'product', 'quantity', 'total_price']

class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Basket
        fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at']
