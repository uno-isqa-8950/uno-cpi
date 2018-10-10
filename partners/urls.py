from django.urls import path
from . import views
app_name = 'partners'

urlpatterns = [

     path('registerCampusPartner/', views.registerCampusPartner, name='registerCampusPartner'),
     path('profile/campuspartneruserprofile/', views.campusPartnerUserProfile, name='campuspartneruserprofile'),
     path('profile/campuspartneruserprofileupdate/', views.campusPartnerUserProfileUpdate, name='campuspartneruserprofileupdate'),
    ]
