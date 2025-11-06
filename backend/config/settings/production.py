"""
Production settings for Beyond Infinity.
These settings are used when deployed to Railway or other production environments.
"""

from .base import *

# Debug mode OFF in production
DEBUG = False

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Email backend - use SMTP in production
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# CORS - restrict to specific origins in production
# Set via environment variable: CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
CORS_ALLOW_ALL_ORIGINS = False

# Cloudinary for media storage in production
if CLOUDINARY_STORAGE['CLOUD_NAME']:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Logging - less verbose in production
LOGGING['root']['level'] = 'WARNING'
LOGGING['loggers']['django']['level'] = 'WARNING'
LOGGING['loggers']['django.request']['level'] = 'ERROR'

# PhonePe - production mode
PHONEPE_CONFIG['ENV'] = config('PHONEPE_ENV', default='PROD')

# Whitenoise for static files (if using)
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

print("Running in PRODUCTION mode")
print(f"PhonePe environment: {PHONEPE_CONFIG['ENV']}")
