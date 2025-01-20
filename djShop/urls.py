from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("authentication.urls")),
    path('store/', include("store.urls")),
    path('basket/', include("basket.urls")),
    path('orders/', include("orders.urls")),
    path('wishlist/', include("wishlist.urls")),
    path('blogs/', include("blog.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)