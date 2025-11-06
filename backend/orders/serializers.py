from rest_framework import serializers
from .models import Order, OrderItem
from addresses.models import Address
from products.serializers import ProductListSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name', 'product_sku', 'size', 'color',
            'quantity', 'price', 'item_total'
        ]

class OrderCreateSerializer(serializers.Serializer):
    address_id = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), source='address')
    coupon_code = serializers.CharField(required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    # The backend will compute cart and prices

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = serializers.StringRelatedField()
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'address', 'items',
            'subtotal', 'discount_amount', 'tax_amount', 'shipping_cost', 'total_amount',
            'payment_status', 'payment_method', 'order_status',
            'tracking_id', 'tracking_url', 'notes', 'created_at', 'updated_at'
        ]
