from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class CreateUserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}