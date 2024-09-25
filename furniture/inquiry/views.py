from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404

from inquiry.serializers import InquirySerializer
from .models import Inquiry
from product.models import Product

# swagger 데코레이터 설정
@swagger_auto_schema(
    method='post',
    operation_id='제품 문의',
    operation_description='제품 문의를 합니다',
    tags=['Inquiry'],
    responses={200: InquirySerializer},
    request_body=InquirySerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])  # JWT 토큰 확인
def inquiry_create(request):
    serializer = InquirySerializer(data=request.data)

    if serializer.is_valid():
        # 유저와 제품 정보를 설정
        serializer.validated_data['user'] = request.user
        serializer.save()  # 문의 저장

        return Response(serializer.data, status=status.HTTP_201_CREATED)  # 성공적으로 생성된 경우

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # 오류 발생 시


@swagger_auto_schema(
    method='put',
    operation_id='제품 문의 내용 수정',
    operation_description='제품 문의 내용을 수정합니다',
    tags=['Inquiry'],
    responses={200: InquirySerializer},
    request_body=InquirySerializer,
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])  # JWT토큰 확인
def inquiry_update(request, pk):
    inq = get_object_or_404(Inquiry, pk=pk)
    serializer = InquirySerializer(instance=inq, data=request.data)

    if serializer.is_valid(raise_exception=True):
        if inq.user == request.user:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else :
            return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

@swagger_auto_schema(
    method='delete',
    operation_id='제품 문의 삭제',
    operation_description='제품 문의를 삭제합니다',
    tags=['Inquiry'],
    responses={200: InquirySerializer}
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def inquiry_delete(request, pk):
    inq = get_object_or_404(Inquiry, pk=pk)

    if inq.user == request.user:
        inq.delete()
        return Response({'message': '삭제 성공'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

@swagger_auto_schema(
    method='get',
    operation_id='해당 제품 문의 리스트 조회',
    operation_description='해당 제품의 전체 문의를 조회합니다',
    tags=['Inquiry'],
    responses={200: InquirySerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])  # 글 확인은 로그인 없이 가능
def inquiry_prod(request, prod_id):
    product = get_object_or_404(Product, pk=prod_id)  # 제품 정보를 가져옴

    # 제품이 비공개인 경우 처리
    if not product.is_public:
        return Response({'message': '비공개된 제품이여서 제품 문의가 공개되지 않습니다.'}, status=status.HTTP_403_FORBIDDEN)

    # 관리자인 경우 모든 문의를, 일반 유저는 공개된 문의만 확인
    if getattr(request.user, 'is_admin', False):  # is_admin 필드를 확인
        prod_list = Inquiry.objects.filter(prod_id=prod_id)  # 관리자일 경우 전체 문의 확인
    else:
        prod_list = Inquiry.objects.filter(prod_id=prod_id, is_public=True)  # 일반 유저는 공개된 문의만 확인

    if not prod_list.exists():
        return Response({'message': '해당 제품에 문의가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = InquirySerializer(prod_list, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(
    method='get',
    operation_id='회원이 쓴 제품 문의 조회',
    operation_description='회원이 쓴 제품 문의 전체 조회',
    tags=['Inquiry'],
    responses={200: InquirySerializer}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def inquiry_list(request):
    # 관리자인 경우 전체 문의, 일반 유저는 본인의 문의만 조회
    if getattr(request.user, 'is_admin', False):  # is_admin 필드를 확인
        inquiries = Inquiry.objects.all()  # 관리자일 경우 모든 문의 조회
    else:
        inquiries = Inquiry.objects.filter(user=request.user)  # 일반 유저는 본인의 문의만 조회

    if not inquiries.exists():
        return Response({'message': '문의가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = InquirySerializer(inquiries, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
