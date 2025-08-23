from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer, NotificationUpdateSerializer
from django.db.models import Q

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_user_notifications(request):
    """Get all notifications for the current user"""
    user = request.user
    
    # Get query parameters
    unread_only = request.query_params.get('unread', '').lower() == 'true'
    notification_type = request.query_params.get('type', None)
    
    # Filter notifications
    notifications = Notification.objects.filter(recipient=user)
    
    if unread_only:
        notifications = notifications.filter(is_read=False)
    
    if notification_type:
        notifications = notifications.filter(notification_type=notification_type)
    
    # Order by timestamp (newest first)
    notifications = notifications.order_by('-timestamp')
    
    serializer = NotificationSerializer(notifications, many=True)
    
    # Count unread notifications
    unread_count = Notification.objects.filter(recipient=user, is_read=False).count()
    
    return Response({
        'notifications': serializer.data,
        'total_count': notifications.count(),
        'unread_count': unread_count,
        'message': f'Found {notifications.count()} notifications'
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_notification_read(request, notification_id):
    """Mark a specific notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.is_read = True
        notification.save()
        
        serializer = NotificationSerializer(notification)
        return Response({
            'detail': 'Notification marked as read',
            'notification': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Notification.DoesNotExist:
        return Response(
            {'detail': 'Notification not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_all_notifications_read(request):
    """Mark all notifications for the current user as read"""
    user = request.user
    
    # Update all unread notifications
    updated_count = Notification.objects.filter(
        recipient=user, 
        is_read=False
    ).update(is_read=True)
    
    return Response({
        'detail': f'Marked {updated_count} notifications as read',
        'updated_count': updated_count
    }, status=status.HTTP_200_OK)

@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_notification(request, notification_id):
    """Delete a specific notification"""
    try:
        notification = Notification.objects.get(id=notification_id, recipient=request.user)
        notification.delete()
        
        return Response({
            'detail': 'Notification deleted successfully'
        }, status=status.HTTP_200_OK)
        
    except Notification.DoesNotExist:
        return Response(
            {'detail': 'Notification not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_notification_stats(request):
    """Get notification statistics for the current user"""
    user = request.user
    
    total_count = Notification.objects.filter(recipient=user).count()
    unread_count = Notification.objects.filter(recipient=user, is_read=False).count()
    
    # Count by type
    type_counts = {}
    for notification_type, _ in Notification.NOTIFICATION_TYPES:
        count = Notification.objects.filter(
            recipient=user, 
            notification_type=notification_type
        ).count()
        type_counts[notification_type] = count
    
    return Response({
        'total_count': total_count,
        'unread_count': unread_count,
        'type_counts': type_counts
    }, status=status.HTTP_200_OK)
