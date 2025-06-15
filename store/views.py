# views_api.py
from rest_framework import generics, permissions,viewsets
from .models import Category, Product, Comment
from .serializers import CategorySerializer, ProductSerializer, CommentSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
import django_filters.rest_framework

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
            'price': ['lt', 'gt', 'exact'],
            'average_rating': ['lt', 'gt', 'exact'],
            'in_stock': ['exact'],
            'is_active': ['exact'],
        }

class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    ordering_fields = ['price', 'average_rating', 'created']
    ordering = ['-created']

    def get_queryset(self):
        queryset = super().get_queryset()
        ordering = self.request.query_params.get('ordering', None)
        if ordering:
            queryset = queryset.order_by(ordering)
        return queryset

    
class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) | Q(description__icontains=search_term) | Q(category__name__icontains=search_term)
            )
        return queryset

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

class ProductCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        comments = Comment.objects.filter(product=product, is_published=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

    def post(self, request, slug):
        
        try:
            product = Product.objects.get(slug=slug)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id, product_id=product_id)
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        if comment.user != request.user:
            return Response({"error": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)