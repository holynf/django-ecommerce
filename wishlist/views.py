from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Wishlist
from .serializers import WishlistSerializer
from store.models import Product
from rest_framework import status
from rest_framework.response import Response

class WishlistView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WishlistSerializer

    def get_object(self):
        wishlist, _ = Wishlist.objects.get_or_create(user=self.request.user)
        return wishlist

    def patch(self, request, *args, **kwargs):
        wishlist = self.get_object()
        item_id = request.data.get('item_id')
        print(item_id)
        
        try:
            item = Product.objects.get(id=item_id)
        except Product.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

        if item in wishlist.products.all():
            wishlist.products.remove(item)
        else:
            wishlist.products.add(item)

        return self.retrieve(request, *args, **kwargs)
