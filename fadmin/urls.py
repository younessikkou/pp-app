"""
URL configuration for pp_admin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import Fadm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Fadm.get, name='home1'),
    path('guichet/', Fadm.guichet, name='home'),
    path('statistics', Fadm.getstatistics, name='statistics'),
    path('guichet', Fadm.guichet, name='guichet'),
    path('submitrapp', Fadm.submitrapp, name='submittrapp'),
    path('delete/<item_id>',Fadm.delete_item, name='delete_item'),  # Corrected
    path('update/<int:item_id>/', Fadm.update_item, name='update_fadmin'),
    path('ajax_pj', Fadm.ajax_pj, name='ajax_pj'),
    path('rech', Fadm.rappsearch, name='cherch'),
    path('searching', Fadm.ajax_search, name='chercher'),
    path('logout', auth_views.LogoutView.as_view(), name='logout'),
    path('recherche', Fadm.recherche, name='recherche'),
    path('rechercherapp', Fadm.ajax_rapport, name='rechercherapp'),
    path('rappdownload', Fadm.rapportdownload, name='rappdownload'),
    path('ihala', Fadm.ihala, name='ihala'),       
]