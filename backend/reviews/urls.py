from django.urls import path
from .views import ProductReviewListAPIView, ProductReviewCreateAPIView, AdminReviewApproveAPIView

urlpatterns = [
    # Public
    path('product/<int:product_id>/', ProductReviewListAPIView.as_view(), name='review-list'),
    path('product/<int:product_id>/add/', ProductReviewCreateAPIView.as_view(), name='review-create'),
    # Admin
    path('admin/<int:pk>/approve/', AdminReviewApproveAPIView.as_view(), name='review-approve'),
]
