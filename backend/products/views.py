from rest_framework import generics, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product, Category
from .serializers import (
    ProductListSerializer, ProductDetailSerializer, ProductCreateUpdateSerializer, CategorySerializer
)

# --- Category Views ---

class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = 'pk'
    permission_classes = [permissions.AllowAny]

# --- Product Views ---

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_featured']
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['base_price', 'discount_price', 'avg_rating', 'created_at']
    permission_classes = [permissions.AllowAny]

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductDetailSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.AllowAny]

# --- Admin/Product Management ---

class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]

class ProductUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateUpdateSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAdminUser]

class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = 'pk'
    permission_classes = [permissions.IsAdminUser]
