from django.db import models
from django.conf import settings


class CartItem(models.Model):
    """Shopping cart items."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE
    )
    quantity = models.IntegerField(default=1)
    size = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=50, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'cart_items'
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = ['user', 'product', 'size', 'color']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.product.name} (x{self.quantity})"
    
    @property
    def subtotal(self):
        """Calculate subtotal for this cart item."""
        return self.product.final_price * self.quantity