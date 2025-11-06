from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_sku', 'quantity', 'price', 'item_total')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'total_amount', 'payment_status', 'order_status', 'created_at')
    list_filter = ('payment_status', 'order_status', 'created_at')
    search_fields = ('order_number', 'user__email', 'tracking_id')
    ordering = ('-created_at',)
    inlines = [OrderItemInline]
    list_editable = ('order_status',)