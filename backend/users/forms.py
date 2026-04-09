from django import forms
from django.contrib.auth.models import User


class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile information."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
        }
