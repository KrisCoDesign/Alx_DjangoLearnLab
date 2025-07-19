from .models import Author, Book, Library, Librarian

books_author = Book.objects.get(Author)

books = Book.objects.all()

librarian = Library.objects.get(Librarian)