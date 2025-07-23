python manage.py shell

from library.models import Book

book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

retrieved_book = Book.objects.get(id=book.id)
print(retrieved_book.title)

retrieved_book.title = "Advanced Django"
retrieved_book.save()

retrieved_book.delete()
