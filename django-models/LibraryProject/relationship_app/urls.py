from django.urls import path
from . import views
from .views import RegisterationView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.list_books, name='list_books'),
    path('<int:pk>/', views.LibraryDetailView.as_view(), 
         name='library_detail'),

    path('register/', RegisterationView.as_view(), name='register'),
    path('login/', LoginView.as_view(
        template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

]
