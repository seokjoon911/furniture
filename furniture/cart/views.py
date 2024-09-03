from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404

from .models import Cart
from cart.serializers import CartSerializer

@swagger_auto_schema(
    method='post',
    operation_id='장바구니 등록',
    operation_description='제품을 장바구니에 등록합니다.',
    tags=['Cart'],
    request_body=CartSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication]) # JWT토큰 확인
def cart_add(request):
    serializer = CartSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='put',
    operation_id='장바구니 수정',
    operation_description='장바구니를 수정합니다.',
    tags=['Cart'],
    request_body=CartSerializer,
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication]) # JWT토큰 확인
def cart_update(request, pk):
    cart = get_object_or_404(Cart, pk=pk)
    serializer = CartSerializer(instance=cart, data=request.data)

    if serializer.is_valid(raise_exception=True):
        if cart.user == request.user:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

@swagger_auto_schema(
    method='delete',
    operation_id='장바구니 삭제',
    operation_description='장바구니에 있는 제품을 삭제합니다',
    tags=['Cart'],
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def cart_delete(request, pk):
    carts = get_object_or_404(Cart, pk=pk)

    if carts.user == request.user:
        carts.delete()
        return Response({'message': '삭제 성공'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

@swagger_auto_schema(
    method='get',
    operation_id='장바구니 조회',
    operation_description='장바구니를 전체 조회합니다.',
    tags=['Cart'],
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication]) # JWT토큰 확인
def cart_list(request):
    try:
        carts = Cart.objects.filter(user=request.user)
        serializer = CartSerializer(carts, many=True)
        return Response(serializer.data)
    except Cart.DoesNotExist:
        return Response({'message': '장바구니에 제품이 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)


