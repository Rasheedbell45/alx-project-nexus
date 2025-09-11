from rest_framework import serializers
from .models import Category, Product
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(write_only=True, source='category', queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ["id", "title", "slug", "description", "price", "in_stock", "created_at", "updated_at", "category", "category_id"]
        read_only_fields = ["id", "created_at", "updated_at"]
