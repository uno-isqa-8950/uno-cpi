from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='base'),
   path('cpi',views.cpipage, name='cpipage'),
   path('registerCampusPartner/', views.registerCampusPartner, name='registerCampusPartner'),
   path('registerCampusPartnerUser/', views.registerCampusPartnerUser, name='registerCampusPartnerUser'),

   ]

