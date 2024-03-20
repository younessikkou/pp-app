from django.shortcuts import render,redirect
from .forms import UserForm
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth import authenticate, login

# Create your views here.


class Auth(APIView):
    def registre(request):
        form = UserForm()
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)  # Log in the user after registration
                redirect('registre')
        return render(request, 'registration.html',{"form":form})

    def login(request):
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")
            else:
                error = 'mot de pass incorrect'
        context = {}
        return render(request, 'login.html', context)