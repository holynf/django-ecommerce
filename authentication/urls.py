from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from authentication.views import CreateUser

urlpatterns = [
    path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', CreateUser.as_view(), name="register_user"),
]