from django.urls import path
from . import views


urlpatterns = [
   path('', views.home, name='home'),
   path('cpi',views.cpipage, name='cpipage'),
   path('registerCampusPartner/', views.registerCampusPartner, name='registerCampusPartner'),
   path('registerCampusPartnerUser/', views.registerCampusPartnerUser, name='registerCampusPartnerUser'),
   path('uploadProject/', views.uploadProject, name='uploadProject'),
   # path('upload_community/', views.uploadCommunity, name='uploadCommunity'),
   # path('upload_campus/', views.uploadCampus, name='uploadCommunity'),
]

