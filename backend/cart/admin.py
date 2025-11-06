from django.contrib import admin
from .models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'size', 'color', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'product__name')
    ordering = ('-created_at',)