from django.contrib import admin
from .models import Book, CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission, Group

class CustomUserAdmin(admin.ModelAdmin):
    # model = CustomUserManager
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser')
admin.site.register(CustomUser, CustomUserAdmin)

# Register your models here.
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author')
    list_filter = ('title', 'author')
admin.site.register(Book, BookAdmin)

# Group and permission creation has been moved to a management command.
# Please use the provided management command to set up groups and assign permissions.

