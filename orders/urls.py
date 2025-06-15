from django.urls import path
from .views import OrderListView,OrderItemView , AddOrderView

urlpatterns = [
    path('', OrderListView.as_view(), name='orders'),
    path('order-items/', OrderItemView.as_view(), name='order-items'),
    path('add-order/',  AddOrderView.as_view(), name='add-order'),
]
