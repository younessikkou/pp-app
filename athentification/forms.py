
# import form class from django 
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

   
# create a ModelForm 
class UserForm(UserCreationForm): 
    # specify the name of model to use 
    email = forms.CharField(max_length=255, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

