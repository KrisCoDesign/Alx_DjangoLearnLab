from django.shortcuts import render
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from .models import Library, Book, Author, UserProfile
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test, permission_required, login_required

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


def is_admin(user):
    return hasattr(user, 'UserProfile') and user.UserProfile.role == 'Admin'
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


def is_librarian(user):
    return hasattr(user, 'UserProfile') and user.UserProfile.role == 'Librarian'
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

def is_member(user):
    return hasattr(user, 'UserProfile') and user.UserProfile.role == 'Member'
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')

@permission_required('relationship_app.can_add_book')
def publish_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    book.published = True
    book.save()
    return redirect('list_books', pk=book.id)

@permission_required('relationship_app.can_change_book')
def book_edit(request, pk):  
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST['title']
        book.author_id = request.POST['author']
        book.save()
        return redirect('list_books', pk=book.id)
    return render(request, 'relationship_app/book_change.html', {'book': book})

@permission_required('relationship_app.can_delete_book')
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return redirect(render,'relationship_app/list_books', {'book': book})

