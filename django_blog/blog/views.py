from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from .models import CustomUser

class RegisterView(CreateView):
    form_class = CustomUser
    success_url = reverse_lazy('login')
    template_name = 'blog/register.html'

class HomeView(TemplateView):
        template_name = 'blog/home.html'

class PostView(TemplateView):
    template_name = 'blog/posts.html'




