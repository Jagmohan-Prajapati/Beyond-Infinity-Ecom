from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import CartItem
from .serializers import CartItemSerializer, CartAddSerializer

class CartListAPIView(generics.ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

class CartAddAPIView(generics.CreateAPIView):
    serializer_class = CartAddSerializer
    permission_classes = [permissions.IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartItemUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartAddSerializer
    lookup_field = 'pk'
    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

class CartClearAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request):
        count, _ = CartItem.objects.filter(user=request.user).delete()
        return Response({'success': True, 'deleted': count})
