from django.contrib import admin
from django.urls import path
from .views import UserRegView

urlpatterns = [
    path('register/', UserRegView.as_view(), name='register')
]