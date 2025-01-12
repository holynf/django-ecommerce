from rest_framework import serializers
from .models import Category, Product, Comment, Discount
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'
        extra_kwargs = {'product': {'write_only': True}}

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'text', 'created_at', 'rating']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

class ProductSerializer(serializers.ModelSerializer):
    discounts = DiscountSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    discounted_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'created_by': {'write_only': True},
            'discounts': {'read_only': True}
        }

    def get_discounted_price(self, obj):
        return obj.get_discounted_price()
