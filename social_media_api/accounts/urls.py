from django.contrib import admin
from django.urls import path
from .views import UserRegView, UserLoginView, UserProfileView, follow_user, unfollow_user
from . import views

urlpatterns = [
    path('register/', UserRegView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),
]