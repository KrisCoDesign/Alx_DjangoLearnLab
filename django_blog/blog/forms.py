from django import forms
from django.contrib.auth.models import User

class RegForm(form.ModelForm):
    class Meta:
        model = User
        fields = ['']
