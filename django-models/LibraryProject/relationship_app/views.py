from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .models import Library, Book, Author
from django.contrib.auth import login

# function based view

def list_books(request):
    books = Book.objects.all()
    authors = Author.objects.all()

    context = {'list_books': books, 'author_list': authors}

    return render(request, 'relationship_app/list_books.html', context)

# class based view

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'

    def get_context_data(self, **kwargs):
        # get default context data
        context = super().get_context_data(**kwargs)
        #retrieve the current library instance
        library = self.get_object()
        context['books'] = library.books.all()
        return context

class register(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')
