from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'actor', 'verb', 'notification_type', 'is_read', 'timestamp']
    list_filter = ['notification_type', 'is_read', 'timestamp']
    search_fields = ['recipient__username', 'actor__username', 'verb']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
