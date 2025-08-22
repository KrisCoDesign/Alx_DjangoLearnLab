from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CustomUser
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserRegSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'bio', 'profile_picture', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match"})
        return attrs
    
    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data['password']
        )
        Token.objects.create(user=user)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User account is disabled.")
                attrs['user'] = user 
                return attrs
            else:
                raise serializers.ValidationError('Invalid username or password.')
            
class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source='followers_count', read_only=True)
    following_count = serializers.IntegerField(source='following_count', read_only=True)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'bio', 
            'profile_picture', 'followers_count', 'following_count', 'date_joined', 'updated_at'
        ]
        read_only_fields = ['id', 'date_joined', 'updated_at',]

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False

class UserProfileSerializer(serializers.ModelSerializer):
    # followers_count = serializers.IntegerField(source='followers_count', read_only=True)
    # following_count = serializers.IntegerField(source='following_count', read_only=True)
    is_following = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 
                  'first_name', 'last_name', 'bio', 'profile_picture', 
                  'followers_count', 'following_count', 'is_following'
                  ]  

    def get_is_following(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False
    
class FollowActionSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        try:
            user = CustomUser.objects.get(id=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
        
        # Prevent users from following themselves
        request_user = self.context['request'].user
        
        if user == request_user:
            raise serializers.ValidationError("You can't follow yourself")
        return value
