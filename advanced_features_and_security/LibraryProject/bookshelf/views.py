from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import ExampleForm

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseForbidden, HttpResponse

@permission_required('bookshelf.can_create', raise_exception=True)
def book_can_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        if title and author and publication_year:
            book = Book(
                title=title,
                author=author,  # This is correct for CharField
                publication_year=publication_year
            )
            book.save()
            return redirect('book_list')
        else:
            return render(request, 'bookshelf/book_create.html', {'error': 'All fields are required.'})
    return render(request, 'bookshelf/book_create.html')

@permission_required('bookshelf.can_edit', raise_exception=True)
def book_can_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        if title and author and publication_year:
            book.title = title
            book.author = author  # This is correct for CharField
            book.publication_year = publication_year
            book.save()
            return redirect('book_list')
        else:
            return render(request, 'bookshelf/book_edit.html', {'book': book, 'error': 'All fields are required.'})
    return render(request, 'bookshelf/book_edit.html', {'book': book})

@permission_required('bookshelf.can_delete', raise_exception=True)
def book_can_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'bookshelf/book_delete.html', {'book': book})

@permission_required('bookshelf.can_view', raise_exception=True)
def book_can_view(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

def form_example(request):
    if request.method == 'POST':
        details = ExampleForm(request.POST)
        if details.is_valid():
            book = details.save(commit=False)
            book.save()
            # redirect it to some another page indicating data
            # was inserted successfully
            return HttpResponse('Data submitted successfully')
        
        else:
            # Redirect back to the same page if the data
            # was invalid
            return render(request, "bookshelf/form_example.html", {'form': details})
    else:
        # If the request is a GET request then,
        # create an empty form object and render it into the page
        form = ExampleForm(None)
        return render(request, 'bookshelf/form_example.html', {'form': form})



