from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from .forms import ProfileForm, UserRegister, PostForm, CommentForm
from .models import get_or_create_profile, Post, Comment


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

@login_required
def profile(request):
     user = request.user
     # Ensure user has a profile
     user_profile = get_or_create_profile(user)
     
     if request.method == 'POST':
          form = ProfileForm(request.POST, request.FILES, instance=user_profile)
          if form.is_valid():
               form.save()
               return redirect('profile')
     else:
         form = ProfileForm(instance=user_profile)
     return render(request, 'blog/profile.html', {'form': form})
               

class CustomLoginView(LoginView):
     template_name = 'blog/login.html'
     redirect_authenticated_user = True

     def get_success_url(self):
         return reverse_lazy('profile')
     
class CustomLogoutView(LogoutView):
     next_page = reverse_lazy('home')


class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'blog/post_list.html'
    ordering = ['-published_date']
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
         context = super().get_context_data(**kwargs)
         context['comments'] = Comment.objects.filter(post=self.get_object()).order_by('-created_at')
         if self.request.user.is_authenticated:
              context['comment_form'] = CommentForm()
         return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/post_detail.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk=self.kwargs['pk'])
        context['comments'] = Comment.objects.filter(post=context['post']).order_by('-created_at')
        return context


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/post_detail.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.post
        context['comments'] = Comment.objects.filter(post=self.object.post).order_by('-created_at')
        context['comment_form'] = self.get_form()
        return context
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/post_detail.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.post
        context['comments'] = Comment.objects.filter(post=self.object.post).order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context