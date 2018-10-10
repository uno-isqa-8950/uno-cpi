from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings


urlpatterns = [

   path('', views.cpipage, name='cpipage'),
   path('home',views.home, name='home'),
   path('campusHome',views.campusHome, name='campusHome'),
   path('map', views.dashboard, name='map'),
   path('about', views.about, name='about'),
   path('registerCampusPartnerUser/', views.registerCampusPartnerUser, name='registerCampusPartnerUser'),
   path('registerCommunityPartnerUser/', views.registerCommunityPartnerUser, name='registerCommunityPartnerUser'),
   path('signupuser/registerCampusPartnerUser/', views.registerCampusPartnerUser, name='registerCampusPartnerUser'),
   path('signupuser/registerCommunityPartnerUser/', views.registerCommunityPartnerUser,name='registerCommunityPartnerUser'),
   path('signup/', views.signup, name='signup'),
   path('signupuser/', views.signupuser, name='signupuser'),
   path('upload_project/', views.upload_project, name='upload_project'),
   path('upload_community/', views.upload_community, name='upload_community'),
   path('upload_campus/', views.upload_campus, name='upload_campus'),

]
