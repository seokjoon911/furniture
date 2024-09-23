from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.inquiry_create, name='inquiry_create'),
    path('inquiry_list/<uuid:prod_id>/', views.inquiry_prod, name='inquiry_prod'), # 제품 문의 전체리스트
    path('inquiry_list/', views.inquiry_list, name='inquiry_list'),
    path('update/<uuid:pk>/', views.inquiry_update, name='inquiry_update'),
    path('delete/<uuid:pk>/', views.inquiry_delete, name='inquiry_delete'),
]