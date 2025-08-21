from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserRegSerializer
from .models import CustomUser
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.shortcuts import get_object_or_404

from .serializers import (
    UserRegSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    UserProfileSerializer,
    FollowActionSerializer,
)

class UserRegView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request):
        serializer = UserRegSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"User Registered Successfully"}, 
                status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'user': UserSerializer(user).data,
            'token': token.key,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    
class UserProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
    def get_serializer_context(self):
        """Pass request context to serializer"""
        return {'request': self.request}
    
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_profile(request):
  "get current users profile"
  serializer = UserSerializer(request.user)
  return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_auth_token(request):
  user = request.user
  token, created = Token.objects.get_or_create(user=user)
  return Response({
      'token': token.key,
      'user_id': user.id,
      'username': user.username
    })

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request):
    """Follow a user. POST /api/accounts/follow/
    Body: {"user_id": 123}"""
    serializer = FollowActionSerializer(
        data=request.data, context={'request': request}
        )

    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        user_to_follow = get_object_or_404(CustomUser, id=user_id)

        # Check if already following
        if request.user.is_following(user_to_follow):
            return Response(
                {"detail": f"You are already following {user_to_follow.username}"}, 
                status=status.HTTP_400_BAD_REQUEST
                )   
        # follow the user
        request.user.follow(user_to_follow)
        
        return Response({
                "detail": f"You are now following {user_to_follow.username}",
                "following": True,
                "followers_count": user_to_follow.followers_count
            }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request):
    """Unfollow a user  POST /api/accounts/unfollow/
    Body: {"user_id": 123}"""
    serializer = FollowActionSerializer(data=request.data, context={'request': request})

    if serializer.is_valid():
        user_id = serializer.validated_data['user_id']
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)

        # Check if actually following
        if not request.user.is_following(user_to_unfollow):
            return Response(
                {"detail": f"You are not following {user_to_unfollow.username}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Unfollow the user
        request.user.unfollow(user_to_unfollow)
        
        return Response({
            "detail": f"You have unfollowed {user_to_unfollow.username}",
            "following": False,
            "followers_count": user_to_unfollow.followers_count
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        