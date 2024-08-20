from django.urls import path
from . import views

urlpatterns = [
    path('toggle/', views.bk_toggle, name='bk_toggle'),
    path('list/', views.bk_list, name='bk_list'),
    path('count/', views.bk_count, name='bk_count'),
]