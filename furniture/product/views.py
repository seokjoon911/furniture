from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser
from .models import Product
from product.serializers import ProdSerializer, ProdDetailSerializer, ProdListSerializer
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from aws_module import upload_to_s3, delete_from_s3
from django.conf import settings
import os, uuid

@swagger_auto_schema(
    method='post',
    operation_id='제품 등록',
    operation_description='제품을 등록합니다',
    tags=['Product'],
    request_body=ProdSerializer,
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])  # JWT토큰 확인
@parser_classes([MultiPartParser])
def prod_create(request):
    request_image = request.FILES.get('image')
    serializer = ProdSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
        prod_obj = serializer.save(user=request.user)

    try:
        if request_image:
            # 파일 이름을 UUID로 생성하고 확장자를 유지
            file_name = str(uuid.uuid4()) + os.path.splitext(request_image.name)[1]

            # aws_module을 이용하여 S3에 사진 업로드
            upload_image = request_image.seek(0)  # 파일 포인터를 맨 처음으로 리셋
            s3_image_url = upload_to_s3(upload_image, file_name)

            # 이미지 URL을 Product 객체에 저장
            prod_obj.url = s3_image_url
            prod_obj.save()

        # 저장된 Product 객체를 다시 직렬화하여 응답으로 보냄
        return Response(ProdSerializer(prod_obj).data, status=status.HTTP_201_CREATED)

    except Exception as e:
        # 예외 발생 시 업로드한 이미지를 삭제 (경로 수정)
        if request_image:
            delete_from_s3(settings.AWS_STORAGE_BUCKET_NAME, prod_obj.url)
        raise exceptions.APIException(str(e))

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
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
    serializer = ProdSerializer(instance=prod, data=request.data, partial=True)  # partial=True로 부분 업데이트 허용

    if serializer.is_valid(raise_exception=True):
        user_email = prod.user.email
        if user_email == request.user.email:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
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
    request_image = request.FILES.get('url')
    old_image_url = prod.url # 기존 사진 URL 저장
    serializer = ProdSerializer(instance=prod, data=request.data, partial=True)  # partial=True로 부분 업데이트 허용

    if serializer.is_valid(raise_exception=True):
        user_email = prod.user.email
        if user_email == request.user.email:
            try:
                # 새로운 이미지가 있으면 기존 이미지 삭제 후 새 이미지 업로드
                if request_image:
                    # 파일 이름을 UUID로 생성하고 확장자를 유지
                    file_name = str(uuid.uuid4()) + os.path.splitext(request_image.name)[1]

                    # 새 이미지 S3 업로드
                    s3_image_url = upload_to_s3(request_image, file_name)

                    # 기존 이미지 삭제
                    if old_image_url:
                        file_name = str(old_image_url).replace(
                            "https://furnitures3.s3.ap-northeast-2.amazonaws.com/images/", "")
                        delete_from_s3(settings.AWS_STORAGE_BUCKET_NAME, file_name)

                    # 새 이미지 URL을 저장
                    serializer.save(url=s3_image_url)

                else:
                    # 이미지가 없으면 기존 이미지를 유지
                    serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                # S3 업로드 중 예외 발생 시 처리
                if request_image:
                    # 업로드된 새 이미지를 삭제
                    delete_from_s3(settings.AWS_STORAGE_BUCKET_NAME, s3_image_url)
                    '''
                    # 기존 이미지를 복원
                    if old_image_url:
                        prod.url = old_image_url
                        prod.save()
                    '''
                return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        if prod.url :
            file_name = str(prod.url).replace("https://furnitures3.s3.ap-northeast-2.amazonaws.com/images/", "")
            delete_from_s3(settings.AWS_STORAGE_BUCKET_NAME, file_name)
        prod.delete()
        return Response({'message': '삭제 성공'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

@swagger_auto_schema(
    method='get',
    operation_id='제품 리스트 조회',
    operation_description='제품 전체를 조회합니다',
    tags=['Product'],
    responses={200: ProdListSerializer},
)
@api_view(['GET'])
@permission_classes([AllowAny])  # 글 확인은 로그인 없이 가능
def prod_list(request):
    prod_list = Product.objects.filter(is_public=True).select_related("user").prefetch_related("category_id")  # is_public이 True인 경우만 조회
    serializer = ProdListSerializer(prod_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_id='제품 조회',
    operation_description='제품 1개 조회',
    tags=['Product'],
    responses={200: ProdDetailSerializer},
)
@api_view(['GET'])
@permission_classes([AllowAny])
def prod_detail(request, pk):
    prod = get_object_or_404(Product, pk=pk)

    if not prod.is_public:
        return Response({"message": "비공개된 제품입니다."}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProdDetailSerializer(prod)
    return Response(serializer.data, status=status.HTTP_200_OK)