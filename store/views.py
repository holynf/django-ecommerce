# views_api.py
from rest_framework import generics, permissions,viewsets
from .models import Category, Product, Comment
from .serializers import CategorySerializer, ProductSerializer, CommentSerializer
from rest_framework.permissions import IsAdminUser

class ProductList(generics.ListAPIView):
    queryset = Product.products.all()   
    serializer_class = ProductSerializer

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.filter(in_stock=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'

class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(product_id=self.kwargs['product_id'], is_published=True)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

class AdminCommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        serializer.save()