from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.review_create, name='review_create'),
]