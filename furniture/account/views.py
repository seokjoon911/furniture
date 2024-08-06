from django.db import transaction
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes, throttle_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from account.serializers import UserSerializer, UserLoginSerializer
from account.models import User
@swagger_auto_schema(
    method='post',
    operation_id='일반 회원가입',
    operation_description='회원가입을 진행합니다.',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description="비밀번호"),
            'pw_confirm': openapi.Schema(type=openapi.TYPE_STRING, description="비밀번호확인"),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description="이름"),
        }
    ),
    tags=['User'],
    responses={200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'access_token': openapi.Schema(type=openapi.TYPE_STRING, description="Access Token"),
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token"),
            }
        )
    )}
)
@api_view(['POST'])
@permission_classes([AllowAny])
@transaction.atomic()
def signup(request):
    """
    email = request.data['body']['email']
    password = request.data['body']['password']
    pw_confirm = request.data['body']['pw_confirm']
    name = request.data['body']['name']
    """
    email = request.data.get('email')
    password = request.data.get('password')
    pw_confirm = request.data.get('pw_confirm')
    name = request.data.get('name')

    try :
        validate_email(email)  # 이메일 주소를 유효성 검사
        if password != pw_confirm:
            return Response({"message": "비밀번호를 다시 확인하세요"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save(email=email, name=name,)  # 필드 값 바로 저장
            user.set_password(password)
            user.save()

    except ValidationError:
        return Response({'message': '유효한 이메일 주소를 입력해주세요.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(method='post', operation_id='로그인', operation_description='로그인을 진행합니다.', request_body=UserLoginSerializer, tags=['User'], )
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    email = request.data['body']['email']
    password = request.data['body']['password']
    """
    email = request.data.get('email')
    password = request.data.get('password')

    user = User.objects.filter(email=email).first()
    if user is not None and user.check_password(password):
        # 추가적인 조건 검사 (예: 이메일 인증 여부)
        if user.is_active:
            # 인증에 성공하고 추가적인 조건도 충족한 경우
            refresh = RefreshToken.for_user(user)
            update_last_login(None, user)

            return Response({'refresh_token': str(refresh),
                             'access_token': str(refresh.access_token),
                             'email': user.email,
                             'name': user.name,
                             }, status=status.HTTP_200_OK)
        else:
            # 인증에는 성공했지만 추가적인 조건을 충족하지 않은 경우 (예: 이메일 미인증)
            return Response({'message': '이메일 인증을 하세요.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        # 인증에 실패한 경우알림
        return Response({'message': '아이디 또는 비밀번호가 일치하지 않습니다.'}, status=status.HTTP_401_UNAUTHORIZED)