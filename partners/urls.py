from django.urls import path, re_path
from . import views

app_name = 'partners'

urlpatterns = [
    path('register-Campus-Partner/', views.registerCampusPartner, name='registerCampusPartner'),
    path('register-Community-Partner/', views.registerCommunityPartner, name='registerCommunityPartner'),
    path('profile/userprofile/', views.userProfile, name='userprofile'),
    path('profile/userprofileupdate/', views.userProfileUpdate, name='userprofileupdate'),
    path('profile/orgprofile/', views.orgProfile, name='orgprofile'),
    re_path(r'^profile/(?P<pk>\d+)/orgprofilecontacts/$', views.orgProfileContacts, name='orgprofilecontact'),
    re_path(r'^profile/(?P<pk>\d+)/orgprofilemissions/$', views.orgProfileMissions, name='orgprofilemission'),
    re_path(r'^profile/(?P<pk>\d+)/orgprofileupdate/$', views.orgProfileUpdate, name='orgprofileupdate'),
    path('orgprofile/partner_add/', views.PartnerAdd, name='partneradd'),
    path('SuggestCommunity/', views.ajax_load_community, name='ajax_load_community'),
    # path('SuggestAcronym/', views.ajax_load_community_acronym, name='ajax_load_community_acronym'),
    path('SuggestCampus/', views.ajax_load_campus, name='ajax_load_campus'),
    path('register-Campus-Partner-For-Project/', views.registerCampusPartner_forprojects,
         name='registerCampusPartnerforprojects'),
    path('register-Community-Partner-For-Project/', views.registerCommunityPartner_forprojects,
         name='registerCommPartnerforprojects'),
    path('check-Community-Partner/', views.checkCommunityPartner, name='checkCommunityPartner')

]
