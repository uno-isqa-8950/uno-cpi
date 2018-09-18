from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views
app_name ='home'

urlpatterns = [

   path('', views.home, name='base'),
   path('cpi',views.cpipage, name='cpipage'),

   ]