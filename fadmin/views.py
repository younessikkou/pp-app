from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Fadmin, Type_pj , Pjs, Type_rapp
from django.core.paginator import Paginator
from .forms import FadminForm
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.core.paginator import Paginator
from django.views.generic import ListView
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from datetime import datetime
import json
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from io import BytesIO






# Create your views here.
class Fadm(APIView):

  def get(request):
    if request.user.is_authenticated:
      fadmin= Fadmin.objects.all()
      typepj= Type_pj.objects.all()
      pj= Pjs.objects.all()
      typerapp= Type_rapp.objects.all()
      context ={} 
      context['form']= FadminForm()
      data = {
        'data0' : typerapp,
        'data1' : fadmin.values(),
        'data2': list(typepj.values()),
        'data3' : pj.values(),
        'form' : FadminForm()
      }
      print(data['data1'])
      return render(request , 'fadmin/recherche.html' , data)
    else:
      return redirect('login')

  def recherche(request):
    startdate = request.POST.get("datedebut")
    enddate = request.POST.get("datefin")
    fadmin= Fadmin.objects.filter(date_arr__range=[enddate, startdate])
    typepj= Type_pj.objects.all()
    typerapp= Type_rapp.objects.all()
    pj= Pjs.objects.all()
    context = {}
    p = Paginator(fadmin, 2)
    page_obj = p.get_page(1)
    if request.method == "GET":
      page_number = request.GET.get("page")
      page_obj = p.get_page(page_number)
    context['form']= FadminForm()
    data = {
      'data0' : typerapp,
      'data1' : fadmin.values(),
      'data2': list(typepj.values()),
      'data3' : pj.values(),
      'form' : FadminForm(),
      "page_obj":page_obj
    }
    return render(request , 'fadmin/recherche2.html' , data)
  
  def ajax_rapport(request):
    startdate = request.POST.get("datedebut")
    enddate = request.POST.get("datefin")
    fadmin= Fadmin.objects.filter(date_arr__range=[startdate,enddate])
    dataajax={}
    dataajax["item"] =list(fadmin.values())
    print(dataajax)
    return JsonResponse(dataajax)
  
  def ajax_pdf(request):
    startdate = request.POST.get("datedebut")
    enddate = request.POST.get("datefin")
    fadmin = Fadmin.objects.filter(date_arr__range=[startdate, enddate])

    # Convertir les données en format JSON
    json_data = json.dumps(list(fadmin.values()), indent=2, cls=DjangoJSONEncoder)

    # Créer un objet BytesIO pour stocker le contenu PDF
    pdf_buffer = BytesIO()

    # Créer le document PDF en utilisant ReportLab
    p = canvas.Canvas(pdf_buffer)
    p.drawString(100, 800, "Données au format JSON :")
    p.drawString(100, 780, json_data)
    p.save()

    # Réinitialiser la position de lecture du buffer PDF à 0
    pdf_buffer.seek(0)

    # Créer un objet HttpResponse avec le type de contenu PDF
    pdf_response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
    pdf_response['Content-Disposition'] = 'inline; filename="rapport.pdf"'

    # Retourner la réponse JSON avec les données JSON
    return JsonResponse({'pdf_data': '', 'json_data': json_data})



  def submitrapp(request):
    # dictionary for initial data with 
    # field names as keys
    context ={}

    # add the dictionary during initialization
    form = FadminForm(request.POST or None)
    if form.is_valid():
      instance = form.save(commit=False)

      # Modification de l'objet
      # hna kansavi form dyal rapp bla type_pj ta nrecuperer type_pj bohdo a partir mn name hiya request.POST.get('type_pj')
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
    else:
      context['error']="form is not valid"
      return render(request,'fadmin/recherche2.html', context)

  @login_required
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


  
  @csrf_exempt
  def ajax_pj(request):
    ab = request.POST.get("ajaxdata")
    print(ab)
    listpj = Pjs.objects.filter(reporter__name_pj=ab)
    print(listpj)
    dataajax = {"list_pj": list(listpj.values('name'))}
    return JsonResponse(dataajax)

  @csrf_exempt
  def ajax_search(request):
    ab = request.POST.get("ajaxdata")
    print('hello im here')
    searching = Fadmin.objects.filter(num_env__icontains=ab)
    print(searching)
    dataajax = {"searching": searching}
    return JsonResponse(dataajax)

  @csrf_exempt
  def chercher(request):
    if request.user.is_authenticated:
      typerapp = request.POST.get("typerapp")
      fadmin= Fadmin.objects.filter(type_rapp=typerapp)
      print(typerapp)
      typepj= Type_pj.objects.all()
      pj= Pjs.objects.all()
      typerapp= Type_rapp.objects.all()
      context ={} 
      context['form']= FadminForm()
      data = {
        'data0' : typerapp,
        'data1' : fadmin.values(),
        'data2': list(typepj.values()),
        'data3' : pj.values(),
        'form' : FadminForm()
      }
      print(data['data1'])
      return render(request , 'fadmin/recherche.html' , data)
    else:
      return redirect('login')

  def rappsearch(request):
    print("im here ------------------ here im")
    typesearch = request.POST.get("typesearch")
    numrapp = request.POST.get("numrapp")
    numplaint = request.POST.get("numplaint")
    typerapp = request.POST.get("typerapp")
    rapp = Type_rapp.objects.all()
    vide= Fadmin.objects.filter(num_rapp_pp__contains='vide')
    typerapp_id = 0
    dataajax={}
    for i in rapp:
      if(i.nom_typerapp==typerapp):
        typerapp_id = i.id
    if(typesearch == "numrapp"):
      print(numrapp)
      fadmin= Fadmin.objects.filter(num_rapp_pp__contains=numrapp) & Fadmin.objects.filter(type_rapp_id=typerapp_id)
      print("-------------"+numrapp)
      if fadmin:
        dataajax["item"] =list(fadmin.values())
      else:
        dataajax["item"] =list(vide.values())
      print(dataajax)
    elif(typesearch == "numplaint"):
      print(numplaint)
      fadmin= Fadmin.objects.filter(num_plaint__contains=numplaint) & Fadmin.objects.filter(type_rapp=typerapp_id)
      print("-------------"+numplaint)
      if fadmin:
        dataajax["item"] =list(fadmin.values())
      else:
        dataajax["item"] =list(vide.values())
      print(dataajax)
    return JsonResponse(dataajax)
    
    


