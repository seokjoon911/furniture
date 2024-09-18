from rest_framework import serializers
from .models import Category, SubCategory

# 카테고리 시리얼라이저
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

# 서브카테고리 시리얼라이저
class SubCategorySerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())  # 카테고리 ID를 받음

    class Meta:
        model = SubCategory
        fields = '__all__'