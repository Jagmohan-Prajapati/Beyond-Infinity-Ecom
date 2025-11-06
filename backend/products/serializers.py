from rest_framework import serializers
from .models import Product, Category
from reviews.models import Review

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'parent', 
            'meta_title', 'meta_description', 'is_active'
        ]

class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'base_price', 'discount_price', 'stock_quantity',
            'is_featured', 'is_active', 'images', 'sizes', 'colors', 'avg_rating', 'review_count'
        ]

class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    reviews = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'base_price', 'discount_price', 'sku',
            'stock_quantity','is_featured','is_active','images','sizes','colors',
            'avg_rating','review_count','description','meta_title','meta_description',
            'created_at','updated_at','reviews'
        ]
    def get_reviews(self, obj):
        reviews = Review.objects.filter(product=obj, is_approved=True)[:5]
        from reviews.serializers import ReviewListSerializer
        return ReviewListSerializer(reviews, many=True).data

class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'category', 'base_price', 'discount_price', 'sku',
            'stock_quantity', 'low_stock_threshold', 'is_featured', 'is_active',
            'images', 'sizes', 'colors', 'description', 'meta_title', 'meta_description'
        ]
