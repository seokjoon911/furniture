from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Category, SubCategory
from .serializers import CategorySerializer, SubCategorySerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.authentication import JWTAuthentication

# 카테고리 등록
@swagger_auto_schema(
    method='post',
    operation_id='카테고리 등록',
    operation_description='새로운 카테고리를 등록합니다.',
    tags=['Category'],
    request_body=CategorySerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 카테고리 작성 가능
@authentication_classes([JWTAuthentication])
def category_create(request):
    serializer = CategorySerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 카테고리 리스트 조회
@swagger_auto_schema(
    method='get',
    operation_id='카테고리 리스트 조회',
    operation_description='모든 카테고리를 조회합니다.',
    tags=['Category'],
    responses={200: CategorySerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([AllowAny])  # 모든 유저가 조회 가능
def category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 카테고리 수정
@swagger_auto_schema(
    method='put',
    operation_id='카테고리 수정',
    operation_description='특정 카테고리를 수정합니다.',
    tags=['Category'],
    request_body=CategorySerializer,
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 수정 가능
@authentication_classes([JWTAuthentication])
def category_update(request, pk):
    category = Category.objects.get(pk=pk)
    serializer = CategorySerializer(category, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

# 카테고리 삭제
@swagger_auto_schema(
    method='delete',
    operation_id='카테고리 삭제',
    operation_description='특정 카테고리를 삭제합니다.',
    tags=['Category'],
    responses={204: 'No Content'}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 삭제 가능
@authentication_classes([JWTAuthentication])
def category_delete(request, pk):
    category = Category.objects.get(pk=pk)
    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# 서브카테고리 등록
@swagger_auto_schema(
    method='post',
    operation_id='서브카테고리 등록',
    operation_description='새로운 서브카테고리를 등록합니다.',
    tags=['SubCategory'],
    request_body=SubCategorySerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 서브카테고리 작성 가능
@authentication_classes([JWTAuthentication])
def subcategory_create(request):
    serializer = SubCategorySerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 서브카테고리 리스트 조회
@swagger_auto_schema(
    method='get',
    operation_id='서브카테고리 리스트 조회',
    operation_description='모든 서브카테고리를 조회합니다.',
    tags=['SubCategory'],
    responses={200: SubCategorySerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([AllowAny])  # 모든 유저가 조회 가능
def subcategory_list(request):
    subcategories = SubCategory.objects.all()
    serializer = SubCategorySerializer(subcategories, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 서브카테고리 수정
@swagger_auto_schema(
    method='put',
    operation_id='서브카테고리 수정',
    operation_description='특정 서브카테고리를 수정합니다.',
    tags=['SubCategory'],
    request_body=SubCategorySerializer,
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 수정 가능
@authentication_classes([JWTAuthentication])
def subcategory_update(request, pk):
    subcategory = SubCategory.objects.get(pk=pk)
    serializer = SubCategorySerializer(subcategory, data=request.data)

    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

# 서브카테고리 삭제
@swagger_auto_schema(
    method='delete',
    operation_id='서브카테고리 삭제',
    operation_description='특정 서브카테고리를 삭제합니다.',
    tags=['SubCategory'],
    responses={204: 'No Content'}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])  # 어드민 유저만 삭제 가능
@authentication_classes([JWTAuthentication])
def subcategory_delete(request, pk):
    subcategory = SubCategory.objects.get(pk=pk)
    subcategory.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
