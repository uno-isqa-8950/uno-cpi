from django.urls import path
from django.conf.urls import url
from . import views
app_name = 'partners'

urlpatterns = [
     path('registerCampusPartner/', views.registerCampusPartner, name='registerCampusPartner'),
     path('registerCommunityPartner/', views.registerCommunityPartner, name='registerCommunityPartner'),
     path('profile/userprofile/', views.userProfile, name='userprofile'),
     path('profile/userprofileupdate/', views.userProfileUpdate,name='userprofileupdate'),
     path('profile/orgprofile/', views.orgProfile, name='orgprofile'),
     url(r'^profile/(?P<pk>\d+)/orgprofilecontacts/$', views.orgProfileContacts, name='orgprofilecontact'),
     url(r'^profile/(?P<pk>\d+)/orgprofileupdate/$', views.orgProfileUpdate, name='orgprofileupdate'),
     path('orgprofile/campus_partner_add/', views.CampusPartnerAdd, name='campuspartneradd'),
	 path('SuggestCommunity/', views.ajax_load_project, name='ajax_load_project'),
     path('registerCampusPartnerForProject/', views.registerCampusPartner_forprojects, name='registerCampusPartnerforprojects'),
     path('registerCommunityPartnerForProject/', views.registerCommunityPartner_forprojects, name='registerCampusPartnerforprojects'),

]
