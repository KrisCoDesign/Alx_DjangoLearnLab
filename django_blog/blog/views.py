from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, UserRegister


class RegisterView(CreateView):
    form_class = UserRegister
    success_url = reverse_lazy('login')
    template_name = 'blog/register.html'

    def form_valid(self, form):
         form.save()
         return super().form_valid(form)


class HomeView(TemplateView):
        template_name = 'blog/home.html'


class PostView(TemplateView):
    template_name = 'blog/posts.html'


class ProfileView(TemplateView):
    template_name = 'blog/profile.html'


@login_required
def profile(request):
     user = request.user
     if request.method == 'POST':
          form = ProfileForm(request.POST, instance=user)
          if form.is_valid():
               form.save()
               return redirect('profile')
     else:
         form = ProfileForm(instance=user)
     return render(request, 'blog/profile.html', {'form': form})
               

class CustomLoginView(LoginView):
     template_name = 'blog/login.html'
     redirect_authenticated_user = True

     def get_success_url(self):
         return reverse_lazy('profile')
     
class CustomLogoutView(LogoutView):
     next_page = reverse_lazy('home')


