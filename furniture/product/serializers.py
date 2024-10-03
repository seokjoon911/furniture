from rest_framework import serializers
from .models import Product
from account.serializers import UserInfoSerializer
from menu.models import SubCategory

class ProdSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)  # 유저 정보를 가져옵니다
    category_name = serializers.CharField(write_only=True)  # 입력받을 하위 카테고리 이름

    class Meta:
        model = Product
        fields = ['user', 'title', 'content', 'category_name', 'price', 'url', 'is_public']

    def create(self, validated_data):
        # 'category_name'은 validated_data에서 제거 후, 카테고리 객체로 변환
        category_name = validated_data.pop('category_name')
        try:
            category = SubCategory.objects.get(name=category_name)
        except SubCategory.DoesNotExist:
            raise serializers.ValidationError({"category_name": "유효한 카테고리명이 아닙니다."})

        validated_data['category_id'] = category  # 카테고리 ID 설정
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # 'category_name' 처리
        category_name = validated_data.pop('category_name', None)
        if category_name:
            try:
                category = SubCategory.objects.get(name=category_name)
            except SubCategory.DoesNotExist:
                raise serializers.ValidationError({"category_name": "유효한 카테고리명이 아닙니다."})

            validated_data['category_id'] = category  # 카테고리 ID 설정

        return super().update(instance, validated_data)

class ProdDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category_id.name', read_only=True)  # 하위 카테고리 이름
    parent_category_name = serializers.CharField(source='category_id.category.name', read_only=True)  # 상위 카테고리 이름

    class Meta:
        model = Product
        fields = ('content', 'url', 'created_at', 'category_name', 'parent_category_name')

class ProdListSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)  # 유저 정보를 가져옵니다
    category_name = serializers.CharField(source='category_id.name', read_only=True)  # 하위 카테고리 이름
    parent_category_name = serializers.CharField(source='category_id.category.name', read_only=True)  # 상위 카테고리 이름

    class Meta:
        model = Product
        fields = ['user', 'title', 'content', 'category_name', 'parent_category_name', 'price', 'url']