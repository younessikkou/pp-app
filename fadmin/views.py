from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Fadmin, Type_pj , Pjs
from django.http import JsonResponse
from django.core.paginator import Paginator
from .forms import FadminForm
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers



# Create your views here.
class Fadm(APIView):
  def get(self, request):
    fadmin= Fadmin.objects.all()
    typepj= Type_pj.objects.all()
    pj= Pjs.objects.all()
    context ={} 
    context['form']= FadminForm()
    data = {
      'data1' : fadmin.values(),
      'data2': list(typepj.values()),
      'data3' : pj.values(),
      'form' : FadminForm()
    }
    print(data['data1'])
    return render(request , 'fadmin/recherche.html' , data)


  def submitrapp(request):
    # dictionary for initial data with 
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    form = FadminForm(request.POST or None)
    instance = form.save(commit=False)

    # Modification de l'objet
    # Par exemple, si vous voulez modifier 'type_pj' à partir de l'ID reçu via POST
    type_pj = request.POST.get('type_pj')
    if type_pj:
      try:
          type_pj_instance = Pjs.objects.get(name=type_pj)
          instance.type_pj = type_pj_instance
      except Pjs.DoesNotExist:
          # Gérer le cas où l'instance Pjs n'existe pas
          context['form'] = form
          context['error'] = "Invalid 'type_pj' selected."
          return render(request, 'recherche.html', context)

  # Enregistrer l'objet après modification
    instance.save()

    return redirect('home')

  def delete_item(request, id):
    item = Fadmin.objects.get(id=id)
    if item:
      try:
        item.delete()
      except item.DoesNotExist:
        context['form'] = form
        context['error'] = "Erreur."
        return render(request, 'recherche.html', context)
    return redirect('home')


  def update_item(request, id):
    context = {}
    item = Fadmin.objects.get(id=id)
    fadmin= Fadmin.objects.all()
    typepj= Type_pj.objects.all()
    pj= Pjs.objects.all()
    data = {
      'data1' : fadmin.values(),
      'data2': list(typepj.values()),
      'data3' : pj.values(),
      'form' : FadminForm(instance=item)
    }
    print(data['data1'])
    return render(request , 'fadmin/recherche.html' , data)

  
  @csrf_exempt
  def ajax_pj(request):
    ab = request.POST.get("ajaxdata")
    print(ab)
    listpj = Pjs.objects.filter(reporter__name_pj=ab)
    print(listpj)
    dataajax = {"list_pj": list(listpj.values('name'))}
    return JsonResponse(dataajax)

