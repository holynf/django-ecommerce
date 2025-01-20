from django.urls import path
from .views import PostViewSet

urlpatterns = [
    path('', PostViewSet.as_view({'get': 'list'}), name='posts'),
    path('<int:pk>/', PostViewSet.as_view({'get': 'retrieve'}), name='post_detail'),
    path('<int:pk>/comments/', PostViewSet.as_view({'get': 'comments'}), name='post_comments'),
]