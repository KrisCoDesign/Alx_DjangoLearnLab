from django.urls import path, include
from . import views
from .views import PostViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

# urlpatterns = [
    # path('post/', views.PostCreateView.as_view(), name='post'),
    # path('comment/', views.CommentCreateView.as_view(), name='comment'),
# ]

routers = DefaultRouter()
routers.register(r'post', PostViewSet, basename='post')
routers.register(r'comment', CommentViewSet, basename='comment')

urlpatterns = [ 
    path('', include(routers.urls)), #routers.urls
]