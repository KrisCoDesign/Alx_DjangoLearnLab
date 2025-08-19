from django.contrib import admin
from django.urls import path
from .views import UserRegView, UserLoginView, UserProfileView

urlpatterns = [
    path('register/', UserRegView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile')
]