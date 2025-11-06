"""
Development settings for Beyond Infinity.
These settings are used during local development.
"""

from .base import *

# Debug mode ON in development
DEBUG = True

# Allowed hosts for development
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']

# Database - using Railway PostgreSQL or local
# Already configured in base.py via DATABASE_URL

# Email backend - print to console in development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS - allow all origins in development (be careful!)
CORS_ALLOW_ALL_ORIGINS = True

# Disable HTTPS requirements in development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Django Debug Toolbar (optional - install if needed)
# INSTALLED_APPS += ['debug_toolbar']
# MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
# INTERNAL_IPS = ['127.0.0.1']

# Cloudinary - use local storage in development
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Logging - more verbose in development
LOGGING['root']['level'] = 'DEBUG'
LOGGING['loggers']['django']['level'] = 'DEBUG'

# PhonePe - ensure UAT mode in development
PHONEPE_CONFIG['ENV'] = 'UAT'

print("Running in DEVELOPMENT mode")
print(f"Email backend: {EMAIL_BACKEND}")
print(f"PhonePe environment: {PHONEPE_CONFIG['ENV']}")
