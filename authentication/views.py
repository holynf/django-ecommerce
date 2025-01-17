from accounts.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from authentication.serializers import UserProfileSerializer, UpdateUserProfileSerializer,UserProfileCustomSerializer


class CreateUser(APIView):

    def post(self, request):
        req_data = request.data

        serializer = UserProfileSerializer(data=req_data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user_data = User(
            username=data["username"],
            email=data["email"],
            last_name=data['last_name'],
            first_name=data['first_name'],
            phone_number=data['phone_number']
        )

        user_data.set_password(data["password"])

        user_data.save()

        return Response(serializer.data)
    
class UserProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserProfileCustomSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        
        user = request.user
        serializer = UpdateUserProfileSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            if 'password' in serializer.validated_data:
                user.set_password(serializer.validated_data['password'])
                user.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)