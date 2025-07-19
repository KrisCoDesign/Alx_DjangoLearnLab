from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Author, Library

# function based view
def list_books(request):
    books = Book.objects.all()
    authors = Author.objects.all()

    context = {'list_books': books, 'author_list': authors}

    return render(request, 'relationship_app/list_books.html', context)

# class based view
def LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/book_detail.html'

    def get_context_data(self, **kwargs):
        # get default context data
        context = super().get_context_data(**kwargs)
        #retrieve the current library instance
        library = self.get_object()
        context['books'] = library.books.all()
        return context