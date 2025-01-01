from django.contrib import admin
from .models import Basket, BasketItem

class BasketItemInline(admin.TabularInline):
    model = BasketItem
    extra = 1  # Number of empty item forms to display in the admin panel
    readonly_fields = ('total_price',)

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Total Price'

@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at', 'total_price')
    search_fields = ('user__username',)
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    inlines = [BasketItemInline]

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Total Price'

@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ('basket', 'product', 'quantity', 'total_price')
    search_fields = ('basket__user__username', 'product__name')
    readonly_fields = ('total_price',)

    def total_price(self, obj):
        return obj.total_price()
    total_price.short_description = 'Total Price'
