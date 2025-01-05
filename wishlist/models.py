from django.db import models
from django.conf import settings
from store.models import Product  # Import the Product model

class Wishlist(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )
    products = models.ManyToManyField(Product, related_name='wishlists')

    def __str__(self):
        return f"{self.user.username}'s Wishlist"
