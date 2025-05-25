from rest_framework import serializers
from .models import Category, CategoryImage
from products.serializers import ProductSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        
class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ['id', 'image', 'is_active', 'category']
        
class CategoryDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)
    images = CategoryImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'product', 'images']