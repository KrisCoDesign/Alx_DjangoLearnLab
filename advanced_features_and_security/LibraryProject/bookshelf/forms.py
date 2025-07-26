from django import forms
from django.core.exceptions import ValidationError
from .models import Employee, Expense, SalaryDetail
import re

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'age', 'job_title', 'emp_type']

    def clean_name(self):
        name = self.cleaned_data['name']
        # Remove leading/trailing whitespace
        name = name.strip()
        # Validate name format (letters, spaces, hyphens, apostrophes)
        if not re.match(r"^[a-zA-Z\s\-']+$", name):
            raise ValidationError("Name contains invalid characters")
        # Prevent excessively long names
        if len(name) > 100:
            raise ValidationError("Name is too long (max 100 characters)")
        return name

    def clean_age(self):
        age = self.cleaned_data['age']
        # Validate age range
        if age < 18 or age > 100:
            raise ValidationError("Age must be between 18 and 100")
        return age

    def clean_job_title(self):
        job_title = self.cleaned_data['job_title']
        # Basic sanitization
        job_title = job_title.strip()
        # Prevent HTML/JS injection
        if re.search(r"<[^>]*>", job_title):
            raise ValidationError("Job title contains invalid characters")
        return job_title


class SalaryForm(forms.ModelForm):
    class Meta:
        model = SalaryDetail
        fields = ['monthly_salary', 'months_worked', 'bonus_percent']

    def clean_monthly_salary(self):
        salary = self.cleaned_data['monthly_salary']
        # Validate salary range
        if salary < 0:
            raise ValidationError("Salary cannot be negative")
        if salary > 1000000:  # Example max value
            raise ValidationError("Salary exceeds maximum allowed")
        return round(salary, 2)  # Sanitize to 2 decimal places

    def clean_months_worked(self):
        months = self.cleaned_data['months_worked']
        # Validate months range
        if months < 0 or months > 12:
            raise ValidationError("Months worked must be between 0 and 12")
        return months

    def clean_bonus_percent(self):
        bonus = self.cleaned_data['bonus_percent']
        # Validate bonus range
        if bonus < 0 or bonus > 100:
            raise ValidationError("Bonus must be between 0% and 100%")
        return round(bonus, 2)  # Sanitize to 2 decimal places


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount']

    def clean_name(self):
        name = self.cleaned_data['name']
        # Sanitize whitespace
        name = name.strip()
        # Validate name format
        if not re.match(r"^[\w\s\-().,'&]+$", name):
            raise ValidationError("Expense name contains invalid characters")
        # Prevent long names
        if len(name) > 255:
            raise ValidationError("Name is too long (max 255 characters)")
        return name

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        # Validate amount
        if amount <= 0:
            raise ValidationError("Amount must be positive")
        if amount > 10000000:  # Example max value
            raise ValidationError("Amount exceeds maximum allowed")
        return round(amount, 2)  # Sanitize to 2 decimal places