from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer, CreateOrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Order, OrderItem
from basket.basket import Basket

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
    
class AddOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)

        if serializer.is_valid():
            data = serializer.validated_data

            order_key = data['order_key']
            full_name = data['full_name']
            address1 = data['address1']
            address2 = data.get('address2', '')
            items = data['items']

            if Order.objects.filter(order_key=order_key).exists():
                return Response(
                    {'error': 'Order with this key already exists.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user_id = request.user.id
            basket = Basket(request)
            basket_total = basket.get_total_price()

            order = Order.objects.create(
                user_id=user_id,
                full_name=full_name,
                address1=address1,
                address2=address2,
                total_paid=basket_total,
                order_key=order_key
            )

            for item in items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )

            return Response(
                {'success': 'Order created successfully', 'order_id': order.id},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)