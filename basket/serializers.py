from rest_framework import serializers
from .models import Basket, BasketItem
from store.serializers import ProductSerializer
from authentication.serializers import UserProfileSerializer

class BasketItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = BasketItem
        fields = ['id', 'product', 'quantity', 'total_price']

class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()
    user = UserProfileSerializer(read_only=True)


    class Meta:
        model = Basket
        fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at']
