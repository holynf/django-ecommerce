from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer,PostCommentSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

# Create your views here.
class PostViewSet(viewsets.ModelViewSet):
    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, slug=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, slug=slug)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, slug=None):
        post = get_object_or_404(Post, slug=slug)
        comments = post.get_comments()
        serializer = PostCommentSerializer(comments, many=True)
        return Response(serializer.data)