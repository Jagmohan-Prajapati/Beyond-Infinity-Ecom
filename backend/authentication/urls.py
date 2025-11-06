"""
URL configuration for authentication app.
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    UserRegistrationView,
    CustomTokenObtainPairView,
    UserLoginView,
    UserLogoutView,
    UserProfileView,
    UserProfileUpdateView,
    ChangePasswordView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    EmailVerificationView,
)

app_name = 'authentication'

urlpatterns = [
    # Registration & Login
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    
    # JWT Token endpoints
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # User Profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile_update'),
    
    # Password Management
    path('password/change/', ChangePasswordView.as_view(), name='change_password'),
    path('password/reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Email Verification
    path('verify-email/', EmailVerificationView.as_view(), name='verify_email'),
]
