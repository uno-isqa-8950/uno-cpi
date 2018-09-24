from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views


urlpatterns = [

   path('', views.cpipage, name='cpipage'),
   path('home',views.home, name='home'),
   path('account',views.home, name='account'),
   path('registerCampusPartner/', views.registerCampusPartner, name='registerCampusPartner'),
   path('registerCampusPartnerUser/', views.registerCampusPartnerUser, name='registerCampusPartnerUser'),
   path('signupuser/registerCampusPartnerUser/', views.registerCampusPartnerUser, name='registerCampusPartnerUser'),
   path('signupuser/registerCommunityPartnerUser/', views.registerCommunityPartnerUser,name='registerCommunityPartnerUser'),
   path('signup', views.signup, name='signup'),
   path('signupuser', views.signupuser, name='signupuser'),
]

