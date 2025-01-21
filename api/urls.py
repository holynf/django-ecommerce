from django.urls import path, include

urlpatterns = [
    path('auth/', include("authentication.urls")),
    path('store/', include("store.urls")),
    path('basket/', include("basket.urls")),
    path('orders/', include("orders.urls")),
    path('wishlist/', include("wishlist.urls")),
    path('blogs/', include("blog.urls")),
]
