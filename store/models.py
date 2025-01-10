from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

class ProductManager(models.Manager):
    def get_queryset(self):
        return super(ProductManager, self).get_queryset().filter(is_active=True)
    

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_creator')
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', default='images/default.png')
    slug = models.SlugField(max_length=255,unique=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    objects = models.Manager()
    products = ProductManager()

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])
    
    def update_average_rating(self):
        comments = self.comments.all()
        if comments.exists():
            total_rating = sum(comment.rating for comment in comments)
            average = total_rating / comments.count()
            self.average_rating = round(average, 2)
        else:
            self.average_rating = 0.00
        self.save()

    def get_discounted_price(self):
        active_discounts = self.discounts.filter(is_active=True)
        price = self.price
        for discount in active_discounts:
            if discount.discount_type == 'percentage':
                price -= price * (discount.value / 100)
            elif discount.discount_type == 'fixed':
                price -= discount.value
        return max(price, 0)

    def __str__(self):
        return self.title
    
class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ],
        default=1
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_average_rating()

    def delete(self, *args, **kwargs):
        product = self.product
        super().delete(*args, **kwargs)
        product.update_average_rating()

    def __str__(self):
        return f'Comment by {self.user.username} on {self.product.slug}'
    
class Discount(models.Model):
    product = models.ForeignKey(Product, related_name='discounts', on_delete=models.CASCADE)
    discount_type = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def is_active(self):
        from django.utils import timezone
        return self.start_date <= timezone.now() <= self.end_date