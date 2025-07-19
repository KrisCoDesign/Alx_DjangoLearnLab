from .models import Author, Book, Library, Librarian

author = Author.objects.get(name="author_name")
books = author.books.all()

library = Library.objects.get(name="library_name")
books = library.books.all()

library = Library.objects.get(name="library_name")
librarian = library.librarian