from rest_framework import serializers
from .models import Notice
from account.serializers import UserInfoSerializer

class NoticeSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = Notice
        fields = '__all__'