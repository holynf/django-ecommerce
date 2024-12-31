# views_api.py
from rest_framework import generics
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.filter(in_stock=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'
