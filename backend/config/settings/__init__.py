"""
Django settings for Beyond Infinity project.
"""
import os

# Determine which settings to use
ENVIRONMENT = os.getenv('DJANGO_ENV', 'development')

if ENVIRONMENT == 'production':
    from .production import *
else:
    from .development import *
