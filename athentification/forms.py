
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    ROLE_CHOICES = (
        ('regular', 'مستعمل عادي'),
        ('admin', 'مدير النظام'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, initial='regular')

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "role"]
