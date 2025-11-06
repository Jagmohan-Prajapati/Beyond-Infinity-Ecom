from django.contrib import admin
from .models import PaymentTransaction


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'order', 'amount', 'status', 'payment_method', 'payment_gateway', 'created_at')
    list_filter = ('status', 'payment_gateway', 'payment_method', 'created_at')
    search_fields = ('transaction_id', 'order__order_number')
    ordering = ('-created_at',)
    readonly_fields = ('transaction_id', 'response_data', 'created_at', 'updated_at')