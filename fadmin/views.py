from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Fadmin
from django.http import JsonResponse
from django.core.paginator import Paginator
from .forms import FadminForm


# Create your views here.
class Fadm(APIView):
  def get(self, request):
    fadmin = Fadmin.objects.all()
    data = {'data' : list(fadmin.values())}
    return render(request , 'fadmin/recherche.html' , data)

  def ajtrapp(request): 
    context ={} 
    context['form']= FadminForm() 
    return render(request, "fadmin/Ajrapp.html", context) 

  def submitrapp(request):
    # dictionary for initial data with 
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = FadminForm(request.POST or None)
    if form.is_valid():
        form.save()
    return redirect('home')