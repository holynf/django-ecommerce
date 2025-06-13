from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from authentication.views import CreateUser, UserProfile,LogoutView

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('register/', CreateUser.as_view(), name="register_user"),
    path('profile/', UserProfile.as_view(), name="register_user"),
]