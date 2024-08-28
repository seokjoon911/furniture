from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser
from .models import Product
from product.serializers import ProdSerializer, ProddetailSerializer
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
@parser_classes([MultiPartParser])
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
@parser_classes([MultiPartParser])
def prod_update(request, pk):
    prod = get_object_or_404(Product, pk=pk)
    serializer = ProdSerializer(instance=prod, data=request.data)

    if serializer.is_valid(raise_exception=True):
        user_email = prod.user.email
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
    user_email = prod.user.email

    if user_email == request.user.email:
        prod.delete()
        return Response({'message': '삭제 성공'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

@swagger_auto_schema(
    method='get',
    operation_id='제품 리스트 조회',
    operation_description='제품 전체를 조회합니다',
    tags=['Product'],
    responses={200: ProdSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])  # 글 확인은 로그인 없이 가능
def prod_list(request):
    prod_list = Product.objects.all()
    serializer = ProdSerializer(prod_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_id='제품 조회',
    operation_description='제품 1개 조회',
    tags=['Product'],
    responses={200: ProddetailSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def prod_detail(request, pk):
    prod = get_object_or_404(Product, pk=pk)
    serializer = ProddetailSerializer(prod)
    return Response(serializer.data, status=status.HTTP_200_OK)