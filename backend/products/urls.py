from django.urls import path
from .views import (
    CategoryListAPIView, CategoryDetailAPIView,
    ProductListAPIView, ProductDetailAPIView,
    ProductCreateAPIView, ProductUpdateAPIView, ProductDeleteAPIView
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),

    # Products
    path('', ProductListAPIView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),

    # Admin
    path('admin/create/', ProductCreateAPIView.as_view(), name='product-create'),
    path('admin/<int:pk>/update/', ProductUpdateAPIView.as_view(), name='product-update'),
    path('admin/<int:pk>/delete/', ProductDeleteAPIView.as_view(), name='product-delete'),
]
