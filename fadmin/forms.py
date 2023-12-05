
# import form class from django 
from django import forms 
   
# import GeeksModel from models.py 
from .models import Fadmin 
   
# create a ModelForm 
class FadminForm(forms.ModelForm): 
    # specify the name of model to use 
    class Meta: 
        model = Fadmin 
        fields = "__all__"