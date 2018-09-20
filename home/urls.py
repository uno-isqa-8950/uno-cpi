from django.urls import path
from . import views


urlpatterns = [
   path('', views.home, name='home'),
   path('cpi',views.cpipage, name='cpipage'),
   path('registerCampusPartner/', views.registerCampusPartner, name='registerCampusPartner'),
   path('registerCampusPartnerUser/', views.registerCampusPartnerUser, name='registerCampusPartnerUser'),
   path('upload/', views.uploadCSV, name='uploadCSV'),
]

