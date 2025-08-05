from django.contrib import admin
from .models import Book, Author

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
admin.site.register(Author, AuthorAdmin)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_year', 'author')
    search_fields = ('title', 'publication_year', 'author__name')
    list_filter = ('publication_year', 'author')
admin.site.register(Book, BookAdmin)

