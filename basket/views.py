from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Basket, BasketItem
from .serializers import BasketSerializer, BasketItemSerializer
from store.models import Product

class BasketView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        basket, _ = Basket.objects.get_or_create(user=request.user)
        serializer = BasketSerializer(basket)
        return Response(serializer.data)

    def post(self, request):
        try:
            if not request.user.is_authenticated:
                return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

            basket, _ = Basket.objects.get_or_create(user=request.user)

            product_id = request.data.get('product_id')
            quantity = int(request.data.get('quantity', 1))

            if not product_id:
                return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

            basket_item, created = BasketItem.objects.get_or_create(basket=basket, product=product)

            if created:
                basket_item.quantity = quantity
            else:
                basket_item.quantity += quantity

            basket_item.save()

            return Response({
                'message': 'Item added to basket' if created else 'Basket updated',
                'item': BasketItemSerializer(basket_item).data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, item_id):
        try:
            if not request.user.is_authenticated:
                return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

            item = BasketItem.objects.get(id=item_id, basket__user=request.user)
            item.delete()
            return Response({'message': 'Item removed from basket'}, status=status.HTTP_204_NO_CONTENT)

        except BasketItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
