from django.urls import path
from . import views
app_name = 'partners'

urlpatterns = [

     path('registerCampusPartner/', views.registerCampusPartner, name='registerCampusPartner'),
     path('profile/userprofile/', views.userProfile, name='userprofile'),
     path('profile/userprofileupdate/', views.userProfileUpdate,name='userprofileupdate'),
     path('registerCommunityPartner/', views.registerCommunityPartner, name='registerCommunityPartner'),
     path('profile/orgprofile/', views.orgProfile, name='orgprofile'),

]
