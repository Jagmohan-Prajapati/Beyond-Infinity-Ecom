"""
Authentication views for Beyond Infinity.
Handles user registration, login, profile, and password operations.
"""

from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

from .serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
    ChangePasswordSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    EmailVerificationSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint.
    Creates new user account and sends verification email.
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Send verification email
        self.send_verification_email(user)
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'message': 'Registration successful. Please check your email to verify your account.',
            'data': {
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_email_verified': user.is_email_verified,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        }, status=status.HTTP_201_CREATED)
    
    def send_verification_email(self, user):
        """Send email verification link to user."""
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Build verification URL (frontend URL)
        verification_url = f"{settings.PHONEPE_CONFIG.get('REDIRECT_URL', 'http://localhost:3000')}/verify-email?token={token}&uid={uid}"
        
        # Render email template
        context = {
            'user': user,
            'verification_url': verification_url,
        }
        
        html_message = render_to_string('emails/verification.html', context)
        plain_message = f"""
        Hi {user.first_name},
        
        Thank you for registering with Beyond Infinity!
        
        Please click the link below to verify your email address:
        {verification_url}
        
        If you didn't create this account, please ignore this email.
        
        Best regards,
        Beyond Infinity Team
        """
        
        send_mail(
            subject='Verify your email - Beyond Infinity',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token obtain view."""
    serializer_class = CustomTokenObtainPairSerializer


class UserLoginView(APIView):
    """
    User login endpoint.
    Returns JWT tokens on successful authentication.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'success': True,
            'message': 'Login successful.',
            'data': {
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_staff': user.is_staff,
                    'is_email_verified': user.is_email_verified,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }
        }, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    """
    User logout endpoint.
    Blacklists the refresh token.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if not refresh_token:
                return Response({
                    'success': False,
                    'error': {'message': 'Refresh token is required.'}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response({
                'success': True,
                'message': 'Logout successful.'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'error': {'message': 'Invalid token or token already blacklisted.'}
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveAPIView):
    """
    Get current user profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserProfileUpdateView(generics.UpdateAPIView):
    """
    Update current user profile.
    """
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'success': True,
            'message': 'Profile updated successfully.',
            'data': UserProfileSerializer(instance).data
        })


class ChangePasswordView(APIView):
    """
    Change user password.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'success': True,
            'message': 'Password changed successfully.'
        }, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    """
    Request password reset.
    Sends reset link to user's email.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        # Generate token and uid
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Build reset URL (frontend URL)
        reset_url = f"{settings.PHONEPE_CONFIG.get('REDIRECT_URL', 'http://localhost:3000')}/reset-password?token={token}&uid={uid}"
        
        # Send email
        context = {
            'user': user,
            'reset_url': reset_url,
        }
        
        html_message = render_to_string('emails/password_reset.html', context)
        plain_message = f"""
        Hi {user.first_name},
        
        You requested to reset your password for Beyond Infinity.
        
        Click the link below to reset your password:
        {reset_url}
        
        If you didn't request this, please ignore this email.
        
        Best regards,
        Beyond Infinity Team
        """
        
        send_mail(
            subject='Reset your password - Beyond Infinity',
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return Response({
            'success': True,
            'message': 'Password reset instructions have been sent to your email.'
        }, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    """
    Confirm password reset with token.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({
                'success': False,
                'error': {'message': 'Invalid reset link.'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify token
        if not default_token_generator.check_token(user, serializer.validated_data['token']):
            return Response({
                'success': False,
                'error': {'message': 'Invalid or expired reset link.'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({
            'success': True,
            'message': 'Password has been reset successfully. You can now login with your new password.'
        }, status=status.HTTP_200_OK)


class EmailVerificationView(APIView):
    """
    Verify user email with token.
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({
                'success': False,
                'error': {'message': 'Invalid verification link.'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify token
        if not default_token_generator.check_token(user, serializer.validated_data['token']):
            return Response({
                'success': False,
                'error': {'message': 'Invalid or expired verification link.'}
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Mark email as verified
        user.is_email_verified = True
        user.save()
        
        return Response({
            'success': True,
            'message': 'Email verified successfully!'
        }, status=status.HTTP_200_OK)
