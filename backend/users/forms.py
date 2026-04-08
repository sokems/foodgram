from django import forms
from django.contrib.auth.models import User


class ProfileEditForm(forms.ModelForm):
    """Форма для обновления юзера"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
        }
