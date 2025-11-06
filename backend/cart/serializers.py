from rest_framework import serializers
from .models import CartItem
from products.serializers import ProductListSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'quantity', 'size', 'color', 'created_at', 'updated_at'
        ]

class CartAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'product', 'quantity', 'size', 'color'
        ]
