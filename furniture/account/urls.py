from django.urls import include, path
from . import views

login_patterns = [
    path('normal/', views.login, name='login'),
]

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', include(login_patterns)),
    path('logout/', views.logout, name='logout'),
    path('delete/', views.delete, name='delete'),
    path('update/', views.update, name='update'),
    path('pw_change/', views.pw_change, name='pw_change'),
    path('check_email/', views.check_email_duplication, name='check_email_duplication'),
    path('refresh_token/', views.refresh_token, name='refresh_token'),
]