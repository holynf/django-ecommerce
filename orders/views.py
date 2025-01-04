from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
    

class OrderListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Order.objects.all()   
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderItemView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)