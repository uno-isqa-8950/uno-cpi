from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
   path('', views.home, name='base'),
   path('cpi',views.cpipage, name='cpipage'),
   path('signup', views.signup, name='signup'),
   path('signupuser', views.signupuser, name='signupuser'),
   path('signup/registerCampusPartner/', views.registerCampusPartner, name='registerCampusPartner'),
   path('registerCampusPartner/', views.registerCampusPartner, name='registerCampusPartner'),
   path('signupuser/registerCampusPartnerUser/', views.registerCampusPartnerUser, name='registerCampusPartnerUser'),
   path('signupuser/registerCommunityPartnerUser/', views.registerCommunityPartnerUser, name='registerCommunityPartnerUser'),

   ]

