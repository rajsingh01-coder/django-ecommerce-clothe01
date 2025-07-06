from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
] 