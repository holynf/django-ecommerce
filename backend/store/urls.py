from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('products/', views.ProductList.as_view(), name='product_all'),
    path('products/search/', views.ProductSearchView.as_view(), name='product_search'),
    path('products/<slug:slug>/', views.ProductDetail.as_view(), name='product_detail'),
    path('products/<slug:slug>/comments/', views.ProductCommentView.as_view(), name='comment-create'),
    path('products/<int:product_id>/comments/<int:comment_id>/', views.ProductCommentView.as_view(), name='comment-delete'),
    path('categories/', views.CategoryList.as_view(), name='category_list')
]