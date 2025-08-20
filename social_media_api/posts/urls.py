from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.PostCreateView.as_view(), name='post'),
    path('comment/', views.CommentCreateView.as_view(), name='comment'),
]