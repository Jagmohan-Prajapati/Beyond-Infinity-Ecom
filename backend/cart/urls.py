from django.urls import path
from .views import (
    CartListAPIView, CartAddAPIView, CartItemUpdateDeleteAPIView, CartClearAPIView
)

urlpatterns = [
    path('', CartListAPIView.as_view(), name='cart-list'),
    path('add/', CartAddAPIView.as_view(), name='cart-add'),
    path('item/<int:pk>/', CartItemUpdateDeleteAPIView.as_view(), name='cart-item-detail'),
    path('clear/', CartClearAPIView.as_view(), name='cart-clear'),
]
