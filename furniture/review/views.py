from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser

from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.http import JsonResponse

from review.serializers import ReviewSerializer
from .models import Review
from product.models import Product

# swagger 데코레이터 설정
@swagger_auto_schema(
    method='post',
    operation_id='리뷰 및 사진 업로드',
    operation_description='리뷰와 사진을 업로드 합니다',
    tags=['Review'],
    responses={200: ReviewSerializer},
    request_body=ReviewSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
@parser_classes([MultiPartParser])
def review_create(request):
    serializer = ReviewSerializer(data=request.data)

    if serializer.is_valid():
        # 유저와 제품 정보를 설정
        serializer.validated_data['user'] = request.user
        serializer.save()  # 리뷰 저장

        return Response(serializer.data, status=status.HTTP_201_CREATED)  # 성공적으로 생성된 경우

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 오류 발생 시


@swagger_auto_schema(
    method='put',
    operation_id='리뷰 수정',
    operation_description='리뷰을 수정합니다',
    tags=['Review'],
    responses={200: ReviewSerializer},
    request_body=ReviewSerializer,
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])  # JWT토큰 확인
@parser_classes([MultiPartParser])
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    serializer = ReviewSerializer(instance=review, data=request.data)

    if serializer.is_valid(raise_exception=True):
        if review.user == request.user:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else :
            return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

@swagger_auto_schema(
    method='delete',
    operation_id='리뷰 삭제',
    operation_description='리뷰를 삭제합니다',
    tags=['Review'],
    responses={200: ReviewSerializer}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.user == request.user:
        review.delete()
        return Response({'message': '삭제 성공'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

@swagger_auto_schema(
    method='get',
    operation_id='해당 제품 리뷰 리스트 조회',
    operation_description='해당 제품의 전체 리뷰를 조회합니다',
    tags=['Review'],
    responses={200: ReviewSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])  # 글 확인은 로그인 없이 가능
def review_prod(request, prod_id):
    product = get_object_or_404(Product, pk=prod_id)  # 제품 정보를 가져옴
    if not product.is_public:  # 제품이 비공개인 경우
        return Response({'message': '비공개된 제품이여서 리뷰가 공개되지 않습니다.'}, status=status.HTTP_403_FORBIDDEN)

    # 관리자는 비공개 리뷰도 볼 수 있음
    if getattr(request.user, 'is_admin', False):
        prod_list = Review.objects.filter(prod_id=prod_id)  # 모든 리뷰 조회
    else:
        prod_list = Review.objects.filter(prod_id=prod_id, is_public=True)  # 공개된 리뷰만 필터링

    if not prod_list.exists():  # 리뷰가 없는 경우
        return Response({'message': '리뷰가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ReviewSerializer(prod_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_id='해당 유저별 리뷰 리스트 조회',
    operation_description='해당 유저별 리뷰 리스트 조회',
    tags=['Review'],
    responses={200: ReviewSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def review_user(request, user):
    # 관리자는 모든 리뷰를 볼 수 있음
    if getattr(request.user, 'is_admin', False):
        users = Review.objects.filter(user=user)  # 해당 유저의 모든 리뷰 조회
    else:
        users = Review.objects.filter(user=user, prod_id__is_public=True)  # 해당 유저의 공개된 리뷰만 조회

    if not users.exists():  # 리뷰가 없는 경우
        return Response({'message': '리뷰가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ReviewSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
"""
    users = Review.objects.filter(user=user)
    serializer = ReviewSerializer(users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)
"""

@swagger_auto_schema(
    method='get',
    operation_id='회원이 쓴 리뷰 조회',
    operation_description='회원이 쓴 리뷰 전체 조회',
    tags=['Review'],
    responses={200: ReviewSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def review_list(request):
    users = Review.objects.filter(user=request.user)
    serializer = ReviewSerializer(users, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_id='제품 평점',
    operation_description='제품의 평균 평점을 반환합니다',
    tags=['Review'],
    responses={200: ReviewSerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def prod_rating_avg(request, prod_id):
    avg_rating = Review.objects.filter(prod_id=prod_id).aggregate(Avg('rating'))['rating__avg']
    return JsonResponse({"average_rating": avg_rating})