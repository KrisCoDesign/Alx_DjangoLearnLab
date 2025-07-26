# forms.py
from django import forms

# Other forms (CustomUserCreationForm, BookForm, etc.)

class ExampleForm(forms.Form):
    # Field definitions
    name = forms.CharField(max_length=100)
    
    # Validation methods
    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            raise ValidationError("Invalid characters")
        return name
    
    # ... other fields and methods ...