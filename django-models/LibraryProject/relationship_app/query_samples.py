from .models import Author, Book, Library, Librarian

author = Author.objects.get(name=author_name)
books = author.objects.filter(author=author)

library = Library.objects.get(name=library_name)
books = library.books.all()

library = Librarian.objects.get(library=library)