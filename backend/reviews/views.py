from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Review
from .serializers import ReviewListSerializer, ReviewCreateSerializer

class ProductReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewListSerializer
    permission_classes = [permissions.AllowAny]
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return Review.objects.filter(product_id=product_id, is_approved=True)

class ProductReviewCreateAPIView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, product_id=self.kwargs['product_id'])

class AdminReviewApproveAPIView(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    permission_classes = [permissions.IsAdminUser]
    def update(self, request, *args, **kwargs):
        review = self.get_object()
        review.is_approved = True
        review.save()
        return Response({"success": True, "message": "Review approved."})
