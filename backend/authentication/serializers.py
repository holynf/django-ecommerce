from rest_framework.serializers import ModelSerializer
from accounts.models import User,UserProfile
from rest_framework import serializers

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password','first_name','last_name','phone_number')
        extra_kwargs = {'password': {'write_only': True}}


class UserProfileCustomSerializer(ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model= UserProfile
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True} , 'user': {'read_only': True}}

class UpdateUserProfileSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        
        instance.save()
        return instance
