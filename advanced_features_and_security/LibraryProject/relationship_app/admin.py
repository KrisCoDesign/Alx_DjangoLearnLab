from django.contrib import admin
from .models import Book, Author, CustomUser
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'author')
    list_filter = ('title', 'author')
admin.site.register(Book, BookAdmin)

class AuthorAdmin(admin.ModelAdmin):
    display = ('name')
admin.site.register(Author, AuthorAdmin)


class CustomUserAdmin(admin.ModelAdmin):
    # model = CustomUserManager
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser')

admin.site.register(CustomUser, CustomUserAdmin)