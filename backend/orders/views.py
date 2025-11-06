from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Order, OrderItem
from .serializers import OrderCreateSerializer, OrderSerializer
from cart.models import CartItem
from coupons.models import Coupon
from decimal import Decimal
from django.db import transaction

class OrderListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderSerializer
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        address = serializer.validated_data['address']
        coupon_code = serializer.validated_data.get('coupon_code')
        notes = serializer.validated_data.get('notes', '')

        user = request.user
        cart_items = CartItem.objects.filter(user=user)
        if not cart_items.exists():
            return Response({'error': 'Cart is empty.'}, status=400)

        # Totals
        subtotal = sum([item.subtotal for item in cart_items])
        discount = Decimal(0)
        coupon = None

        if coupon_code:
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                if coupon.usage_limit and coupon.used_count >= coupon.usage_limit:
                    raise Exception("Coupon usage limit reached.")
                if coupon.min_order_value and subtotal < coupon.min_order_value:
                    raise Exception("Order does not meet the minimum for coupon.")
                discount = coupon.discount_value if coupon.discount_type == 'FIXED' else (subtotal * coupon.discount_value/Decimal(100))
                if coupon.max_discount_amount: discount = min(discount, coupon.max_discount_amount)
                coupon.used_count += 1
                coupon.save()
            except Exception as e:
                return Response({'error': str(e)}, status=400)

        tax = subtotal * Decimal('0.18')  # GST 18%
        shipping = Decimal('0.00')
        total = subtotal + tax + shipping - discount

        order = Order.objects.create(
            user=user,
            address=address,
            coupon=coupon,
            subtotal=subtotal,
            discount_amount=discount,
            tax_amount=tax,
            shipping_cost=shipping,
            total_amount=total,
            notes=notes,
            payment_status='PENDING',
            order_status='PENDING'
        )

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                product_sku=item.product.sku,
                size=item.size,
                color=item.color,
                quantity=item.quantity,
                price=item.product.final_price,
                item_total=item.subtotal,
            )
            # Deduct stock
            item.product.stock_quantity -= item.quantity
            item.product.save()

        cart_items.delete()

        return Response(OrderSerializer(order).data, status=201)

class OrderDetailAPIView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        qs = super().get_queryset()
        # Allow user to access only their orders, admin can see all
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)
