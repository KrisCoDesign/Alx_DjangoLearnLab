# forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Book
import re
from datetime import date

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        help_text="Your password must contain at least 8 characters including letters and numbers."
    )
    
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
        help_text="Enter the same password as before for verification."
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'date_of_birth', 'profile_photo')

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        # Alphanumeric + underscores only
        if not re.match(r'^[\w.@+-]+\Z', username):
            raise ValidationError(
                "Username can only contain letters, numbers, and @/./+/-/_ characters."
            )
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters long.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower().strip()
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use.")
        return email

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        if dob:
            today = date.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            
            if age < 13:
                raise ValidationError("You must be at least 13 years old to register.")
            if dob.year < 1900:
                raise ValidationError("Please enter a valid birth year.")
        return dob

    def clean_profile_photo(self):
        photo = self.cleaned_data['profile_photo']
        if photo:
            # Check file extension
            valid_extensions = ['.jpg', '.jpeg', '.png', '.gif']
            if not any(photo.name.lower().endswith(ext) for ext in valid_extensions):
                raise ValidationError("Unsupported file format. Supported formats: JPG, PNG, GIF.")
            
            # Check file size (max 2MB)
            if photo.size > 2 * 1024 * 1024:
                raise ValidationError("File size too large. Max 2MB allowed.")
        return photo

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            # Minimum length
            if len(password1) < 8:
                raise ValidationError("Password must be at least 8 characters long.")
            
            # Complexity requirements
            if not any(char.isdigit() for char in password1):
                raise ValidationError("Password must contain at least one number.")
                
            if not any(char.isalpha() for char in password1):
                raise ValidationError("Password must contain at least one letter.")
                
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords don't match")
            
        return cleaned_data


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'date_of_birth', 'profile_photo')

    # Reuse validation from creation form where applicable
    clean_username = CustomUserCreationForm.clean_username
    clean_email = CustomUserCreationForm.clean_email
    clean_date_of_birth = CustomUserCreationForm.clean_date_of_birth
    clean_profile_photo = CustomUserCreationForm.clean_profile_photo


# class BookForm(forms.ModelForm):
class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
    
    def clean_title(self):
        title = self.cleaned_data['title'].strip()
        if len(title) < 2:
            raise ValidationError("Title must be at least 2 characters long.")
            
        # Prevent HTML/JS injection
        if re.search(r'<[^>]*>', title):
            raise ValidationError("Title contains invalid characters.")
            
        return title

    def clean_author(self):
        author = self.cleaned_data['author'].strip()
        if len(author) < 2:
            raise ValidationError("Author name must be at least 2 characters long.")
            
        # Allow letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s\-'.]+$", author):
            raise ValidationError("Author name contains invalid characters.")
            
        return author

    def clean_publication_year(self):
        year = self.cleaned_data['publication_year']
        current_year = date.today().year
        
        # Validate year range
        if year < 1800 or year > current_year + 1:
            raise ValidationError(
                f"Publication year must be between 1800 and {current_year + 1}"
            )
            
        return year