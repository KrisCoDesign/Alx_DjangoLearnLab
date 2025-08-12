from django.urls import path
from blog.views import RegisterView
# from django.contrib.auth.views import LogoutView, LoginView
from .views import HomeView, PostView, ProfileView, CustomLoginView, CustomLogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register/', RegisterView.as_view(), name='register' ),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page='home'), name='logout'),
    path('post/', PostView.as_view(), name='posts'),
    path('profile/', ProfileView.as_view(), name='profile'),
    
]
