from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.prod_create, name='prod_create'),
    path('update/<uuid:pk>', views.prod_update, name='prod_update'),
    path('delete/<uuid:pk>', views.prod_delete, name='prod_delete'),
    path('list/', views.prod_list, name='prod_list'),
    path('detail/<uuid:pk>', views.prod_detail, name='prod_detail'),
]