from django.urls import path
from .views import OrderListView,OrderItemView 

urlpatterns = [
    path('', OrderListView.as_view(), name='orders'),
    path('order-items/', OrderItemView.as_view(), name='order-items'),
]
