from rest_framework import serializers
from .models import Basket, BasketItem
from store.serializers import ProductSerializer

class BasketItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = BasketItem
        fields = ['id', 'product', 'quantity', 'total_price']

class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()


    class Meta:
        model = Basket
        fields = ['id', 'items', 'total_price', 'updated_at']
