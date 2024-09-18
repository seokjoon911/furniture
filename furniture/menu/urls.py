from django.urls import path
from . import views

urlpatterns = [
    # 카테고리 관련 URL
    path('categories/', views.category_list, name='category_list'),  # 카테고리 리스트 조회
    path('categories/create/', views.category_create, name='category_create'),  # 카테고리 등록
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),  # 카테고리 수정
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),  # 카테고리 삭제

    # 서브카테고리 관련 URL
    path('subcategories/', views.subcategory_list, name='subcategory_list'),  # 서브카테고리 리스트 조회
    path('subcategories/create/', views.subcategory_create, name='subcategory_create'),  # 서브카테고리 등록
    path('subcategories/<int:pk>/update/', views.subcategory_update, name='subcategory_update'),  # 서브카테고리 수정
    path('subcategories/<int:pk>/delete/', views.subcategory_delete, name='subcategory_delete'),  # 서브카테고리 삭제
]