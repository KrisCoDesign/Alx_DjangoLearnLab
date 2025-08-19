from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserRegSerializer
from .models import CustomUser
from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from .serializers import (
    UserRegSerializer, 
    UserLoginSerializer, 
    UserSerializer,
    UserProfileSerializer,
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
            'message': 'Login sucessful'
        }, status=status.HTTP_200_OK)
    
class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
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