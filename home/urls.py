from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views
#app_name = home

urlpatterns = [
   path('', views.cpipage, name='cpipage'),
   path('home',views.home, name='home'),
   path('registerCampusPartner/', views.registerCampusPartner, name='registerCampusPartner'),
   path('registerCampusPartnerUser/', views.registerCampusPartnerUser, name='registerCampusPartnerUser'),

   ]

