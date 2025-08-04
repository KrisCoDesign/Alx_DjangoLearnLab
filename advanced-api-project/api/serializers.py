from rest_framework import serializers
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']

    def validation(self, obj):
        if obj['publication_year'] > 2025:
            raise serializers.ValidationError("Year is above 2025.")
        return obj

class AuthorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Author
        fields = ['name']