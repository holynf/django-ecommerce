from rest_framework import serializers
from .models import Category , Comment , Post
from authentication.serializers import UserProfileSerializer

class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    categories = PostCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class PostCommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = "__all__"

class PostCommentListSerializer(serializers.ModelSerializer):
    comments = PostCommentSerializer(many=True,read_only=True)

    class Meta:
        model = Post
        fields = "__all__"