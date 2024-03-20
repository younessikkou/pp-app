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
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
import json
from django.http import HttpResponse, JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from io import BytesIO
from django.template.loader import render_to_string
from weasyprint import HTML
import xlsxwriter
from django.contrib.messages import add_message
from django.contrib import messages 







# Create your views here.
class Fadm(APIView):

  def get(request):
    if request.user.is_authenticated:
      fadmin= Type_rapp.objects.all()
      pj= Pjs.objects.all()
      typerapp= Type_rapp.objects.all()
      typepj= Type_pj.objects.all()
      sayr= Fadmin.objects.filter(type_rapp=1).count()
      osra= Fadmin.objects.filter(type_rapp=2).count()
      chikayamo= Fadmin.objects.filter(type_rapp=3).count()
      chikayaadiya= Fadmin.objects.filter(type_rapp=4).count()
      print(chikayaadiya)
      print(sayr)
      print(osra)
      print(chikayamo)
      context ={} 
      context['form']= FadminForm()
      data = {
        'sayr' : sayr,
        'osra' : osra,
        'chikayamo' : chikayamo,
        'chikayaadiya' : chikayaadiya,
        'data0' : typerapp,
        'data1' : fadmin.values(),
        'data2': list(typepj.values()),
        'data3' : pj.values(),
        'form' : FadminForm()
      }
      return render(request , 'fadmin/index.html' , data)
    else:
      return redirect('login')

  def getstatistics(request):
    if request.POST.get("source") == "load":
      aujourdhui = datetime.today()
      enddate = aujourdhui.strftime('%Y-%m-%d')
      startdate = aujourdhui - timedelta(days=30) 
      startdate = startdate.strftime('%Y-%m-%d')
      sayr= Fadmin.objects.filter(date_arr__range=[startdate,enddate]).filter(type_rapp=1).count()
      osra= Fadmin.objects.filter(date_arr__range=[startdate,enddate]).filter(type_rapp=2).count()
      chikayamo= Fadmin.objects.filter(date_arr__range=[startdate,enddate]).filter(type_rapp=3).count()
      chikayaadiya= Fadmin.objects.filter(date_arr__range=[startdate,enddate]).filter(type_rapp=4).count()
      dataajax={}
      dataajax["sayr"]= sayr
      dataajax["osra"]= osra
      dataajax["chikayamo"]= chikayamo
      dataajax["chikayaadiya"]= chikayaadiya
    else:
      startdate = request.POST.get("datedebut")
      enddate = request.POST.get("datefin")
      sayr= Fadmin.objects.filter(date_arr__range=[startdate,enddate]).filter(type_rapp=1).count()
      osra= Fadmin.objects.filter(date_arr__range=[startdate,enddate]).filter(type_rapp=2).count()
      chikayamo= Fadmin.objects.filter(date_arr__range=[startdate,enddate]).filter(type_rapp=3).count()
      chikayaadiya= Fadmin.objects.filter(date_arr__range=[startdate,enddate]).filter(type_rapp=4).count()
      dataajax={}
      dataajax["sayr"]= sayr
      dataajax["osra"]= osra
      dataajax["chikayamo"]= chikayamo
      dataajax["chikayaadiya"]= chikayaadiya
    return JsonResponse(dataajax)


  def guichet(request):
    if request.user.is_authenticated:
      fadmin= Fadmin.objects.filter()
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
    fadmin= Fadmin.objects.filter(date_arr__range=[startdate,enddate])
    print(fadmin)
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
    typerapp = request.POST.get("typerapp")
    fadmin= Fadmin.objects.filter(date_arr__range=[startdate,enddate]).filter(type_rapp=typerapp)
    dataajax={}
    dataajax["item"] =list(fadmin.values())
    print(dataajax)
    return JsonResponse(dataajax)
  

  def submitrapp(request):
    # dictionary for initial data with 
    # field names as keys
    context ={}

    # add the dictionary during initialization
    form = FadminForm(request.POST or None)
    type_pj = request.POST.get('num_rapp_pj')
    fadmin = Fadmin.objects.all()
    pjs = Pjs.objects.all()
    for p in pjs:
      if p.indice == type_pj:
         type_pj = p.name   
    for f in fadmin:
      print("im testing -----")
      print(type_pj)
      print(f.type_pj)
      if f.type_pj==type_pj:
          context['error'] = "هذا المحضر موجود في عاقدة البيانات"
          return render(request,'fadmin/recherche2.html', context)

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
        add_message(request, messages.SUCCESS, 'لقد تمت الاضافة بنجاح')
        return redirect('home')
      else:
        context['error']="form is not valid"
        return render(request,'fadmin/recherche2.html', context)

  @login_required
  def delete_item(request, item_id):
    item = Fadmin.objects.get(id=item_id)
    if item:
      try:
        item.delete()
      except item.DoesNotExist:
        context['form'] = form
        context['error'] = "Erreur."
        return render(request, 'recherche.html', context)
    return redirect('home1')


  
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
    num_rapppj = request.POST.get("num_rapppj")
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
    elif(typesearch == "numrapppj"):
      print(num_rapppj)
      fadmin= Fadmin.objects.filter(num_rapp_pj__contains=num_rapppj) & Fadmin.objects.filter(type_rapp=typerapp_id)
      print("-------------"+num_rapppj)
      if fadmin:
        dataajax["item"] =list(fadmin.values())
      else:
          dataajax["item"] =list(vide.values())
      print(dataajax)
    return JsonResponse(dataajax)
    
    
  def ihala(request):
    startdate = request.POST.get("datedebut")
    enddate = request.POST.get("datefin")
    typerapp = request.POST.get("typerapp")
    fadmin= Fadmin.objects.filter(date_arr__range=[startdate,enddate]).filter(type_rapp=typerapp)
    textihala = request.POST.get("textihala")
    ids = request.POST.getlist('id[]')
    for f in fadmin:
        for i in ids:    
            if str(f.id) == i:
                # Mettez à jour le champ note avec la valeur de textihala
                f.note = "تمت الاحالة على " + textihala 
                f.save()  # Enregistrez les modifications dans la base de données
                print("Champ note mis à jour pour l'ID", f.id)
        
    dataajax = {"message" : "boucle terminer"}
    return JsonResponse(dataajax)


  @csrf_exempt
  def rapportdownload(request):
    startdate = request.POST.get("datedebut")
    enddate = request.POST.get("datefin")
    typerapp = request.POST.get("typerapp")
    data = Fadmin.objects.filter(date_arr__range=[startdate, enddate]).filter(type_rapp=typerapp)

    # Rendu des données dans un template HTML
    html_string = render_to_string('rapp_pdf.html', {'data': data})

    # Création du fichier PDF avec WeasyPrint
    pdf_file = HTML(string=html_string).write_pdf()

    # Réponse HTTP avec le PDF en pièce jointe
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="donnees.pdf"'
    return response



  def update_item(request, item_id):
    fadmin = Fadmin.objects.get(id=item_id)

    if request.method == 'POST':
      # Create a form instance with the POST data and the existing object instance
      form = FadminForm(request.POST, instance=fadmin)
      if form.is_valid():
        form.save()
        # Success message or redirection after successful update
        add_message(request, messages.SUCCESS, 'لقد تم التغيير بنجاح')
        return redirect('home')  # Replace with your desired redirect URL
      else:
        # Handle form validation errors
        context = {'form': form, 'errors': form.errors}
        return render(request, 'fadmin/update_form.html', context)
    else:
      # GET request, populate the form with existing data
      form = FadminForm(instance=fadmin)
      context = {'form': form}
      return render(request, 'fadmin/update_form.html', context)