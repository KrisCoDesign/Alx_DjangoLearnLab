from django import forms
from django.forms import ModelForm
from .models import Book

class ExampleForm(ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

    # function for validation
    def clean(self):
        super(ExampleForm, self).clean()
        title = self.cleaned_data.get('title')
        publication_year = self.cleaned_data.get('publication_year')

        if title and len(title) < 5:
            self.add_error('title', "Minimum of 5 characters required")

        if publication_year and publication_year >= 2000:
            self.add_error('publication_year', 'Publication year must be before the year 2000')

        return self.cleaned_data

        