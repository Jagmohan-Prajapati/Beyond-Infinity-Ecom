"""
Custom User model for Beyond Infinity.
Extends Django's AbstractUser with additional fields.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    """
    Custom user model with email as the primary identifier.
    """
    email = models.EmailField(
        unique=True,
        db_index=True,
        help_text="User's email address (used for login)"
    )
    
    phone = PhoneNumberField(
        blank=True,
        null=True,
        help_text="User's phone number with country code"
    )
    
    is_email_verified = models.BooleanField(
        default=False,
        help_text="Whether the user has verified their email"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Make email the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """Return the user's full name."""
        return f"{self.first_name} {self.last_name}".strip() or self.email
    
    @property
    def is_verified(self):
        """Check if user is verified."""
        return self.is_email_verified
