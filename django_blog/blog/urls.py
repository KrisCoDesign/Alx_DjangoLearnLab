from django.urls import path

from blog.views import (
    RegisterView, HomeView, PostView, CustomLoginView, CustomLogoutView, 
    profile, PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView, SearchResultsView, TaggedPostListView
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
    path('post/<int:pk>/comments/new/', CommentCreateView.as_view(), name='comment_create'),
    path('post/comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('post/comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

    # Tagged posts and search
    path('tag/<slug:slug>/', TaggedPostListView.as_view(), name='tagged'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]
