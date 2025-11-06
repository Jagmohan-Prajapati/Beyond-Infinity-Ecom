from django.contrib import admin
from .models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'city', 'state', 'is_default', 'address_type', 'created_at')
    list_filter = ('is_default', 'address_type', 'state', 'created_at')
    search_fields = ('user__email', 'full_name', 'city', 'postal_code')
    ordering = ('-created_at',)