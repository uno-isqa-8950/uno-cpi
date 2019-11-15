from django.urls import path


from django.conf.urls.static import static
from . import views
from django.conf import settings


urlpatterns = [

   path('campusHome',views.campusHome, name='campusHome'),
   path('CommunityHome',views.CommunityHome, name='CommunityHome'),
   path('partners/',views.partners,name='partners'),
   path('map', views.countyData, name='map'),
   path('registerCampusPartnerUser/', views.registerCampusPartnerUser, name='registerCampusPartnerUser'),
   path('registerCommunityPartnerUser/', views.registerCommunityPartnerUser, name='registerCommunityPartnerUser'),
   path('signupuser/registerCampusPartnerUser/', views.registerCampusPartnerUser, name='registerCampusPartnerUser'),
   path('signupuser/registerCommunityPartnerUser/', views.registerCommunityPartnerUser,name='registerCommunityPartnerUser'),
   path('signup/', views.signup, name='signup'),
   path('signupuser/', views.signupuser, name='signupuser'),
   path('uploadProject/', views.upload_project, name='upload_project'),
   path('uploadCommunity/', views.upload_community, name='upload_community'),
   path('uploadCampus/', views.upload_campus, name='upload_campus'),
   path('uploadIncome/', views.upload_income, name='upload_income'),
   path('mission-chart/', views.missionchart, name='missionchart'),
   path('issue-address/', views.issueaddress, name='issueaddress'),
   path('network-analysis/', views.networkanalysis, name='networkanalysis'),
   path('trend-report/', views.trendreport, name='trendreport'),
   path('partnership-intensity/', views.partnershipintensity, name='partnershipintensity'),
   path('project-Info/', views.project_partner_info, name='project_partner_info'),
   path('engage-Type/', views.engagement_info, name='engagement_info'),
   path('engagement-type-chart2/' , views.EngagementType_Chart, name = 'EngagementType_Chart'),
   path('AdminHome/', views.AdminHome , name= 'adminhome'),
   path('Adminframe/', views.Adminframe, name='Adminframe'),
   path('recentchanges/', views.recentchanges, name='recentchanges' ),
   path('thanks/', views.thanks, name='thanks'),
   path('inviteCommunityPartnerUser/', views.invitecommunityPartnerUser, name='invitecommunityPartnerUser'),
   path('projectMap', views.googleprojectdata, name='googleprojectmap'),
   path('legislativeDistrict', views.googleDistrictdata, name='googleDistrictmap'),
   path('communityPartner', views.googlepartnerdata, name='googlehomepage'),
   path('communityPartnerType', views.googlemapdata, name='googlemap'),
   path('activate/<str:uidb64>/<str:token>', views.activate, name='activate'),
   path('inviteCommPartner/<str:uidb64>/<str:token>', views.registerCommPartner, name='inviteCommPartner'),
   path('inviteCommPartner/done/<str:pk>/', views.commPartnerResetPassword, name='commPartnerResetPassword')
]
