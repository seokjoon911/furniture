from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.cart_add, name='cart_add'),
    path('update/<uuid:pk>/', views.cart_update, name='cart_update'),
    path('delete/<uuid:pk>/', views.cart_delete, name='cart_delete'),
    path('list/', views.cart_list, name='cart_list'),
]