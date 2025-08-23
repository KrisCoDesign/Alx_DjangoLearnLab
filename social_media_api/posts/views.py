from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer, LikeSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification

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
        comment = serializer.save(author=self.request.user)
        
        # Create notification for post author (if not commenting on own post)
        if comment.post.author != self.request.user:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb="commented on your post",
                notification_type='comment',
                content_type=ContentType.objects.get_for_model(Comment),
                object_id=comment.id
            )

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

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, pk):
    """Like a post"""
    post = generics.get_object_or_404(Post, pk=pk)

    user = request.user
    
    # Check if user already liked the post
    if Like.objects.filter(post=post, user=user).exists():
        return Response(
            {"detail": "You have already liked this post"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create the like
    like = Like.objects.create(post=post, user=user)
    
    # Create notification for post author (if not liking own post)
    if post.author != user:
        Notification.objects.create(
            recipient=post.author,
            actor=user,
            verb="liked your post",
            notification_type='like',
            content_type=ContentType.objects.get_for_model(Post),
            object_id=post.id
        )
    
    return Response({
        "detail": "Post liked successfully",
        "like": LikeSerializer(like).data
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unlike_post(request, pk):
    """Unlike a post"""
    post = get_object_or_404(Post, id=pk)
    user = request.user
    
    # Check if user has liked the post
    try:
        like = Like.objects.get(post=post, user=user)
        like.delete()
        return Response({
            "detail": "Post unliked successfully"
        }, status=status.HTTP_200_OK)
    except Like.DoesNotExist:
        return Response(
            {"detail": "You haven't liked this post"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_post_likes(request, post_id):
    """Get all likes for a specific post"""
    post = get_object_or_404(Post, id=post_id)
    likes = post.likes.all()
    serializer = LikeSerializer(likes, many=True)
    
    return Response({
        "post_id": post_id,
        "likes_count": likes.count(),
        "likes": serializer.data
    }, status=status.HTTP_200_OK)