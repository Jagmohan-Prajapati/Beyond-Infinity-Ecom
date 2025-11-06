from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Coupon(models.Model):
    """Discount coupons."""
    
    DISCOUNT_TYPES = [
        ('PERCENTAGE', 'Percentage'),
        ('FIXED', 'Fixed Amount'),
    ]
    
    code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField(blank=True)
    
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    min_order_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    max_discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    
    usage_limit = models.IntegerField(
        null=True,
        blank=True,
        help_text="NULL means unlimited usage"
    )
    used_count = models.IntegerField(default=0)
    
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    
    is_active = models.BooleanField(default=True, db_index=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_coupons'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'coupons'
        verbose_name = 'Coupon'
        verbose_name_plural = 'Coupons'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.code