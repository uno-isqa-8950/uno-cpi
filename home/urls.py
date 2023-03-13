from django.urls import path, re_path

from django.conf.urls.static import static
from . import views
from django.conf import settings

urlpatterns = [

   path('campusHome',views.campusHome, name='campusHome'),
   path('CommunityHome',views.CommunityHome, name='CommunityHome'),
   path('partners/',views.partners,name='partners'),
   path('map', views.countyData, name='map'),
   path('register-Campus-Partner-User/', views.registerCampusPartnerUser, name='registerCampusPartnerUser'),
   path('registerCommunityPartnerUser/', views.registerCommunityPartnerUser, name='registerCommunityPartnerUser'),
   path('signupuser/registerCampusPartnerUser/', views.registerCampusPartnerUser, name='registerCampusPartnerUser'),
   path('signupuser/registerCommunityPartnerUser/', views.registerCommunityPartnerUser,name='registerCommunityPartnerUser'),
   path('signup/', views.signup, name='signup'),
   path('signupuser/', views.signupuser, name='signupuser'),
   path('uploadProject/', views.upload_project, name='upload_project'),
   path('uploadCommunity/', views.upload_community, name='upload_community'),
   path('uploadCampus/', views.upload_campus, name='upload_campus'),
   path('uploadIncome/', views.upload_income, name='upload_income'),
   path('missionchart/', views.missionchart, name='missionchart'),
   path('issueaddress/', views.issueaddress, name='issueaddress'),
   path('networkanalysis/', views.networkanalysis, name='networkanalysis'),
   path('trendreport/', views.trendreport, name='trendreport'),
   path('partnershipintensity/', views.partnershipintensity, name='partnershipintensity'),
   #path('projectInfo/', views.primary_focus_topic_info, name='primary_focus_topic_info'),
   path('projectInfo_public/', views.project_partner_info_public, name='project_partner_info_public'),
   path('projectInfo_admin/', views.project_partner_info_admin, name ='project_partner_info_admin' ),
   path('engage-Type/', views.engagement_info, name='engagement_info'),
   path('engagementtypechart2/' , views.EngagementType_Chart, name = 'EngagementType_Chart'),
   path('Admin-frame/', views.Adminframe, name='Adminframe'),
   path('thanks/', views.thanks, name='thanks'),
   path('invite-Community-Partner-User/', views.invitecommunityPartnerUser, name='invitecommunityPartnerUser'),
   path('project-Map', views.googleprojectdata, name='googleprojectmap'),
   path('legislative-District', views.googleDistrictdata, name='googleDistrictmap'),
   path('city-District', views.googlecityDistrict, name='googlecityDistrict' ),
   path('community-Partner', views.googlepartnerdata, name='googlehomepage'),
   path('community-Partner-Type', views.googlemapdata, name='googlemap'),
   path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
   path('inviteCommPartner/<str:uidb64>/<str:token>', views.registerCommPartner, name='inviteCommPartner'),
   path('inviteCommPartner/done/<str:pk>/', views.commPartnerResetPassword, name='commPartnerResetPassword'),
   path('recent-changes/',views.recentchanges,name ='recent_changes'),
   re_path(r'^uploadSubCategoires/(?P<pk>\d+)/$',views.uploadProjectSub,name='uploadProjectSub'),
   re_path(r'^deleteProjSub/$',views.removeExistingProjSub,name='removeExistingProjSub')
]
