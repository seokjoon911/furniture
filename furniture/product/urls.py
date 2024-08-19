from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.prod_create, name='prod_create'),
]