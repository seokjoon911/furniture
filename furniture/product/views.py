from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Product
from product.serializers import ProdSerializer
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404

@swagger_auto_schema(
    method='post',
    operation_id='제품 등록',
    operation_description='제품을 등록합니다',
    tags=['Product'],
    request_body=ProdSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication]) # JWT토큰 확인
def prod_create(request):
    serializer = ProdSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(status=status.HTTP_201_CREATED)

@swagger_auto_schema(
    method='put',
    operation_id='제품 수정',
    operation_description='제품을 수정합니다',
    tags=['Product'],
    responses={200: ProdSerializer},
    request_body=ProdSerializer,
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])  # JWT토큰 확인
def prod_update(request, pk):
    prod = get_object_or_404(Product, pk=pk)
    serializer = ProdSerializer(instance=prod, data=request.data)

    if serializer.is_valid(raise_exception=True):
        product = Product.objects.get(prod_id=prod.prod_id)
        user_email = product.user.email
        if user_email == request.user.email:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else :
            return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

@swagger_auto_schema(
    method='delete',
    operation_id='제품 삭제',
    operation_description='제품을 삭제합니다',
    tags=['Product'],
    responses={200: ProdSerializer},
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])  # JWT토큰 확인
def prod_delete(request, pk):
    prod = get_object_or_404(Product, pk=pk)
    product = Product.objects.get(prod_id=prod.prod_id)
    user_email = product.user.email

    if user_email == request.user.email:
        prod.delete()
        return Response({'message': '삭제 성공'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)