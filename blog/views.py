from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer,PostCommentListSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        comments = post.get_comments()
        serializer = PostCommentListSerializer(comments, many=True)
        return Response(serializer.data)