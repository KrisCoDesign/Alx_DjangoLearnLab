from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Author, Library

# function based view
def book_view(request):
    books = Book.objects.all()
    authors = Author.objects.all()

    context = {'book_list': books, 'author_list': authors}

    return render(request, 'books/book_list.html', context)

# class based view
def LibraryDetailView(DetailView):
    model = Library
    template_name = 'books/book_detail.html'

    def get_context_data(self, **kwargs):
        # get default context data
        context = super().get_context_data(**kwargs)
        #retrieve the current library instance
        library = self.get_object()
        context['books'] = library.books.all()
        return context