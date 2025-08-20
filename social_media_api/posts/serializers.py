from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', 
                                            read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'title', 'content', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        Attach the logged-in user as author and create the Post.
        Expect the view to pass request in serializer context:
        serializer = PostSerializer(data=request.data, context={'request': request})
        """
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username',
                                               read_only=True)
    post_id = serializers.IntegerField(source='post.id', read_only=True)
    
    class Meta:
        model = Comment
        field = ['id', 'post', 'post_id', 'author', 'author_username', 'content', 'created_at', 'update_at']

        def create(self, validated_data):
            request = self.context.get('request')
            if request and hasattr(request, 'user'):
                validated_data['author'] = request.user
            return super().create(validated_data)
