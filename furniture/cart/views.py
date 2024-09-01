from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from cart.serializers import CartSerializer
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(
    method='post',
    operation_id='제품 장바구니 등록',
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