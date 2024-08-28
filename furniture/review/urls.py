from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.review_create, name='review_create'),
    path('prod_list/<uuid:prod_id>/', views.review_list, name='review_list'),
    path('prod_user/<str:user>/', views.review_user, name='review_user'),
    path('update/<uuid:pk>/', views.review_update, name='review_update'),
    path('delete/<uuid:pk>/', views.review_delete, name='review_delete'),
    path('prod_rate/<uuid:prod_id>/', views.prod_rating_avg, name='prod_rating_avg'),
]