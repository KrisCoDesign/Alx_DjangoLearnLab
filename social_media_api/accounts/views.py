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
    # UserLoginSerializer, 
    # UserSerializer,
    # UserProfileSerializer
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
