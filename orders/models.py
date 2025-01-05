from decimal import Decimal
from django.conf import settings
from django.db import models

from store.models import Product

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('shipped', 'Shipped'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
    full_name = models.CharField(max_length=50)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    post_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=5, decimal_places=2)
    order_key = models.CharField(max_length=200, unique=True)
    billing_status = models.BooleanField(default=False)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f"Order {self.id} - {self.created.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def calculate_total(self):
        return sum(item.price * item.quantity for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"OrderItem {self.id} - Product: {self.product.title}, Quantity: {self.quantity}"