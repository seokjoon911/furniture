from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Product
from product.serializers import ProdSerializer
from django.db import connections
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='post',
    operation_id='제품 등록',
    operation_description='제품을 등록합니다',
    tags=['Product'],
    request_body=ProdSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication]) # JWT 토큰 확인
def prod_create(request):
    serializer = ProdSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        # 인증객체를 통해 인증을 진행하고 사용자 정보를 request.user 객체에 저장
        # 인증정보가 없거나 일치하지않으면 AnonymousUser를 저장
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED)
