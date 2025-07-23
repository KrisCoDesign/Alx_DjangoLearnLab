from django.contrib import admin
from .models import Book, Author
# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'author')
    list_filter = ('title', 'author')
admin.site.register(Book, BookAdmin)

class AuthorAdmin(admin.ModelAdmin):
    display = ('name')
admin.site.register(Author, AuthorAdmin)