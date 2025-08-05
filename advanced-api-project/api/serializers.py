from rest_framework import serializers
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    
    def validate_publication_year(self, value):
        if value > 2025:
            raise serializers.ValidationError("Year is above 2025.")
        return value

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']