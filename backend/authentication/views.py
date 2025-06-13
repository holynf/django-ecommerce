from accounts.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
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
    
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({"detail": "Refresh token not provided."}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"detail": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)