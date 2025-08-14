from django.urls import path
from blog.views import (
    RegisterView, HomeView, PostView, CustomLoginView, CustomLogoutView, 
    profile, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', profile, name='profile'),
    
    # Post CRUD URLs
    path('post/', PostListView.as_view(), name='post_list'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    
    # Legacy URL for backward compatibility
    path('post/', PostView.as_view(), name='posts'),

    # comment section
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('post/<int:pk>/comment/', CommentUpdateView.as_view(), name='comment_update'),
    path('post/<int:pk>/comment/', CommentDeleteView.as_view(), name='comment_delete'),
]
