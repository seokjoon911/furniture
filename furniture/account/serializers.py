from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        name = data.get('name')

        if get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "이미 존재하는 이메일입니다."})

        if get_user_model().objects.filter(name=name).exists():
            raise serializers.ValidationError({"name": "이미 존재하는 이름입니다."})

        return data

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'name',)

class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email','password')