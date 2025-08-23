from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_user_notifications, name='get-notifications'),
    path('stats/', views.get_notification_stats, name='notification-stats'),
    path('mark-all-read/', views.mark_all_notifications_read, name='mark-all-read'),
    path('<int:notification_id>/mark-read/', views.mark_notification_read, name='mark-notification-read'),
    path('<int:notification_id>/delete/', views.delete_notification, name='delete-notification'),
]
