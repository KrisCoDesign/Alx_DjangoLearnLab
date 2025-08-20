from django.shortcuts import render
from rest_framework import generics, permissions
from .serializers import PostSerializer, CommentSerializer
# from rest_framework.decorators import permission_classes

class PostCreateView(generics.CreateAPIView):
    # queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CommentCreateView(generics.CreateAPIView):
    Serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]