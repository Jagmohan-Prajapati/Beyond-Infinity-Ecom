from rest_framework import serializers
from .models import Review
from authentication.models import User

class ReviewListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'rating', 'comment', 'is_verified_purchase',
            'is_approved', 'created_at'
        ]
    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "email": obj.user.email,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name
        }

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
