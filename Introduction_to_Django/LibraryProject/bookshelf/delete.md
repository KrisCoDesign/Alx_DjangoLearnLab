book.delete()

// expected output

book = Book.objects.get(id=book.id)  
print(book.title, book.author, book.publication_year)

// expected ouput
