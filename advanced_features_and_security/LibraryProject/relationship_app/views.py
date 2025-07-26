from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .models import Library, Book, Author, UserProfile
from django.contrib.auth import login
from django.contrib.auth.decorators import permission_required, user_passes_test, login_required


# function based view

def list_books(request):
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'relationship_app/list_books.html', context)

# class based view

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        context['library'] = library
        return context

class register(CreateView):
    form_class = UserCreationForm
    template_name = 'relationship_app/register.html'
    success_url = reverse_lazy('login')


def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

@permission_required('relationship_app.can_add_book')
def add_book(request, book_id):
    # This function should create a new book, not modify existing
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        if title and author_id:
            author = get_object_or_404(Author, pk=author_id)
            book = Book.objects.create(title=title, author=author)
            return redirect('list_books')
    return render(request, 'relationship_app/add_book.html')

@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):  
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author_id = request.POST['author']
        book.save()
        return redirect('list_books')
    return render(request, 'relationship_app/book_change.html', {'book': book})

@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/list_books.html', {'books': Book.objects.all()})

