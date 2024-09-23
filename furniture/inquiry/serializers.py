from rest_framework import serializers
from .models import Inquiry
from account.serializers import UserInfoSerializer

class InquirySerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True) # 유저 정보를 가져온다.

    class Meta:
        model = Inquiry
        fields = '__all__'