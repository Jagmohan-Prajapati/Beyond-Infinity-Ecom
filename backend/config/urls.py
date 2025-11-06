"""
URL configuration for Beyond Infinity project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Beyond Infinity API",
        default_version='v1',
        description="E-commerce API for Beyond Infinity clothing store",
        contact=openapi.Contact(email="contact@beyondinfinity.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API v1
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/products/', include('products.urls')),
    path('api/v1/reviews/', include('reviews.urls')),
    path('api/v1/cart/', include('cart.urls')),
    path('api/v1/orders/', include('orders.urls')),
    # More app URLs will be added here in next packages
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
