from django.urls import path
from . import views
from .views import register, admin_view, librarian_view, member_view
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.list_books, name='list_books'),
    path('<int:pk>/', views.LibraryDetailView.as_view(), 
         name='library_detail'),

    path('register/', views.register.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    path('admin/', views.admin_view, name='admin'),
    path('librarian/', views.librarian_view, name='librarian'),
    path('member/', views.member_view, name='member'),

     # Permission-protected Book actions
    path('book/<int:book_id>/add_book/', views.add_book, name='add_book'),
    path('book/<int:pk>/edit_book/', views.edit_book, name='edit_book'),
    path('book/<int:pk>/delete_book/', views.delete_book, name='delete_book'),
]
