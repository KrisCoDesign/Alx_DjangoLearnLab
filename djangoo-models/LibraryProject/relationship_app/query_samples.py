from library.models import Author, Book, Library, Librarian

author_john = Book.objects.filter(field_name='john')

books = Library.objects.prefetch_related('books')

Librarian = Librarian.objects.get()