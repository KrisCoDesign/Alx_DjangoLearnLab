from django.urls import path
from blog.views import RegisterView
from django.contrib.auth.views import LoginView, LogoutView
from .views import HomeView, PostView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register' ),
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('post/', PostView.as_view(), name='posts'),
  
    
]
