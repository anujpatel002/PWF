from rest_framework import serializers
from .models import Product, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model            = Review
        fields           = ['id', 'product', 'user_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['created_at']


class ProductSerializer(serializers.ModelSerializer):
    # Nested serializer: embed reviews list inside each product response
    reviews     = ReviewSerializer(many=True, read_only=True)
    # Computed field: average rating
    avg_rating  = serializers.SerializerMethodField()

    class Meta:
        model  = Product
        fields = ['id', 'name', 'description', 'price', 'image', 'reviews', 'avg_rating']

    def get_avg_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return None
        return round(sum(r.rating for r in reviews) / len(reviews), 1)
