from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'address1', 'city', 'total_paid', 'billing_status', 'created', 'updated']
    list_filter = ['billing_status', 'created', 'updated']
    search_fields = ['full_name', 'address1', 'city', 'phone', 'post_code']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)