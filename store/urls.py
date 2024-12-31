from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='product_all'),
    path('products/<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
    path('categories/', views.CategoryList.as_view(), name='category_list')
]