from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        name = data.get('name')
        nickname = data.get('nickname')

        if get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "이미 존재하는 이메일입니다."})

        return data

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'name', 'nickname', 'address')

class UserLoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email','password',)

class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'name', 'nickname','address',)

    def update(self, instance, validated_data):
        # 비밀번호가 제공된 경우 해시하고 저장
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        return super(UserUpdateSerializer, self).update(instance, validated_data)

class UserPwchangeSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    new_pw = serializers.CharField(write_only=True)
    pw_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('password', 'new_pw', 'pw_confirm',)

class UserPwresetSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email','name')

class UseremailcheckSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email',)

class UsernicknamecheckSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('nickname',)

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'name', 'nickname',)

class TokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()