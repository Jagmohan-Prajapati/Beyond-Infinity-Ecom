from django.contrib import admin
from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'discount_value', 'used_count', 'usage_limit', 'valid_from', 'valid_until', 'is_active')
    list_filter = ('discount_type', 'is_active', 'created_at')
    search_fields = ('code', 'description')
    ordering = ('-created_at',)
    list_editable = ('is_active',)