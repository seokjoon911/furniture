from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser

from review.serializers import ReviewSerializer
from .models import Review

from drf_yasg.utils import swagger_auto_schema

"""
import uuid, os
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django.http import JsonResponse
from django.db import transaction
from django.conf import settings
"""

# swagger 데코레이터 설정
@swagger_auto_schema(
    method='post',
    operation_id='리뷰 및 사진 업로드',
    operation_description='리뷰와 사진을 업로드 합니다',
    tags=['Review'],
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