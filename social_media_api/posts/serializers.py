from rest_framework import serializers
from .models import Post, Comment, Like

class LikeSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'user_username', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', 
                                            read_only=True)
    author = serializers.ReadOnlyField(source='author.id')
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'title', 'content', 'created_at', 'updated_at', 'likes_count', 'is_liked']

        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False

    def create(self, validated_data):
        """
    Attach the logged-in user as author and create the Post.Expect the view to pass request in serializer context:
    serializer = PostSerializer(data=request.data, context={'request': request})
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username',
                                               read_only=True)
    author = serializers.ReadOnlyField(source='author.id')
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)


    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'post', 'author_username', 'created_at']

        read_only_fields = ['id', 'post', 'author', 'created_at', 'updated_at']

        def create(self, validated_data):
            request = self.context.get('request')
            post = self.context.get('post')
            if request and hasattr(request, 'user'):
                validated_data['author'] = request.user
            if post:
                validated_data['post'] = post
            return super().create(validated_data)
