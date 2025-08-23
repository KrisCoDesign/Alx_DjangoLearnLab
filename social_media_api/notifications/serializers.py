from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)
    target_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'recipient_username', 'actor', 'actor_username',
            'verb', 'notification_type', 'target_info', 'timestamp', 'is_read'
        ]
        read_only_fields = ['id', 'timestamp']
    
    def get_target_info(self, obj):
        """Get information about the target object"""
        if obj.target:
            try:
                if hasattr(obj.target, 'title'):
                    return {'type': 'post', 'title': obj.target.title}
                elif hasattr(obj.target, 'content'):
                    return {'type': 'comment', 'content': obj.target.content[:50] + '...' if len(obj.target.content) > 50 else obj.target.content}
                else:
                    return {'type': 'unknown', 'id': obj.object_id}
            except:
                return {'type': 'unknown', 'id': obj.object_id}
        return None

class NotificationUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating notification read status"""
    
    class Meta:
        model = Notification
        fields = ['is_read']
