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
     url(r'^profile/(?P<pk>\d+)/orgprofilemissions/$', views.orgProfileMissions, name='orgprofilemission'),
     url(r'^profile/(?P<pk>\d+)/orgprofileupdate/$', views.orgProfileUpdate, name='orgprofileupdate'),
     path('orgprofile/partner_add/', views.PartnerAdd, name='partneradd'),
	 path('SuggestCommunity/', views.ajax_load_community, name='ajax_load_community'),
     path('SuggestCampus/', views.ajax_load_campus, name='ajax_load_campus'),
     path('registerCampusPartnerForProject/', views.registerCampusPartner_forprojects, name='registerCampusPartnerforprojects'),
     path('registerCommunityPartnerForProject/', views.registerCommunityPartner_forprojects, name='registerCampusPartnerforprojects'),
     path('checkCommunityPartner/', views.checkCommunityPartner, name='checkCommunityPartner')

]
