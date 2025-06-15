from django.contrib import admin

from .models import Category, Product, Comment,Discount


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id",'title', 'author', 'slug', 'price',
                    'in_stock', 'created', 'updated']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'text', 'created_at', 'is_published')
    list_filter = ('is_published', 'product')
    search_fields = ('text', 'user__username')
    ordering = ('-created_at',)

    def get_queryset(self, request):
        return super().get_queryset(request)

@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'product')

    def get_queryset(self, request):
        return super().get_queryset(request)