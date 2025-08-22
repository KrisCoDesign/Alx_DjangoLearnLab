from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.db.models import Q

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    """Get posts from users that the current user follows"""
    user = request.user
    
    # Get posts from users that the current user follows
    following_users = user.following.all()
    
    # Get posts from followed users, ordered by creation date (newest first)
    feed_posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
    
    # Serialize the posts
    serializer = PostSerializer(feed_posts, many=True, context={'request': request})
    
    return Response({
        'posts': serializer.data,
        'count': feed_posts.count(),
        'message': f'Showing posts from {following_users.count()} users you follow'
    }, status=status.HTTP_200_OK)