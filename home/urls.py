from django.urls import path
from django.conf.urls.static import static
from . import views


urlpatterns = [

   path('', views.cpipage, name='cpipage'),
   path('home',views.home, name='home'),
   path('registerCampusPartner/', views.registerCampusPartner, name='registerCampusPartner'),
   path('registerCampusPartnerUser/', views.registerCampusPartnerUser, name='registerCampusPartnerUser'),
   path('registerCommunityPartnerUser/', views.registerCommunityPartnerUser, name='registerCommunityPartnerUser'),
   path('signupuser/registerCampusPartnerUser/', views.registerCampusPartnerUser, name='registerCampusPartnerUser'),
   path('registerCommunityPartner/',views.registerCommunityPartner, name='registerCommunityPartner'),
   path('signupuser/registerCommunityPartnerUser/', views.registerCommunityPartnerUser,name='registerCommunityPartnerUser'),
   path('signup/', views.signup, name='signup'),
   path('signupuser/', views.signupuser, name='signupuser'),
   path('uploadProject/', views.uploadProject, name='uploadProject'),
   path('uploadCommunity/', views.uploadCommunity, name='uploadCommunity'),
   path('uploadCampus/', views.uploadCampus, name='uploadCampus'),
]
