from django.db import models


class PaymentTransaction(models.Model):
    """Payment transactions via PhonePe gateway."""
    
    STATUS_CHOICES = [
        ('INITIATED', 'Initiated'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('PENDING', 'Pending'),
    ]
    
    order = models.ForeignKey(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    
    transaction_id = models.CharField(max_length=255, unique=True, db_index=True)
    payment_gateway = models.CharField(max_length=50, default='PHONEPE')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='INITIATED')
    payment_method = models.CharField(max_length=50, blank=True)  # UPI, CARD, WALLET, etc.
    
    response_data = models.JSONField(default=dict, blank=True)  # Store full gateway response
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payment_transactions'
        verbose_name = 'Payment Transaction'
        verbose_name_plural = 'Payment Transactions'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['order']),
        ]
    
    def __str__(self):
        return f"{self.transaction_id} - {self.status}"