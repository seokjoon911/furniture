from rest_framework import serializers
from .models import Product
from account.serializers import UserInfoSerializer

class ProdSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True) # 유저 정보를 가져옵니다

    class Meta:
        model = Product
        fields = '__all__'