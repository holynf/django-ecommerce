from django.db import models
from accounts.models import User 
from store.models import Product

class Wishlist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )
    products = models.ManyToManyField(Product, related_name='wishlists')

    def __str__(self):
        return f"{self.user.username}'s Wishlist"
