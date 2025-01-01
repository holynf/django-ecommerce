from django.urls import path
from .views import BasketView

urlpatterns = [
    path('', BasketView.as_view(), name='basket'),
    path('item/<int:item_id>/', BasketView.as_view(), name='basket-item'),
]
