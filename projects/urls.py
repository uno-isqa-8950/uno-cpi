from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf.urls import url
# app_name = 'projects'

urlpatterns = [
    path('communitypartnerproject/', views.communitypartnerproject, name='communitypartnerproject'),
    url(r'^project/(?P<pk>\d+)/edit/$', views.editProject, name='editProject'),
    url(r'^createProject/$', views.createProject, name='createProject'),
    url(r'^SuggestProject/$', views.ajax_load_project, name='ajax_load_project'),
    # path('SuggestProject/', views.ajax_load_project, name='ajax_load_project'),
    url(r'^projectadd/$', views.project_total_Add, name='projectadd'),
    path('myProjects/',views.myProjects, name='myProjects'),
    path('allProjects/', views.showAllProjects, name='showAllProjects'),
    url(r'^projectSearchAdd/(?P<pk>\d+)/', views.SearchForProjectAdd, name='projectSearchAdd'),
    path('projectspublicreport/', views.projectsPublicReport, name='projectspublicreport'),
    path('projectspublictableview/',views.projectstablePublicReport,name='projectspublictableview'),
    url(r'^projectsfromMissionReport/(?P<pk>\d+)/', views.projectsfromMissionReport, name='projectsfromMissionReport'),
    url(r'^communityfromMissionReport/(?P<pk>\d+)/', views.communityfromMissionReport, name='communityfromMissionReport'),
    path('communitypublicreport/', views.communityPublicReport, name='communitypublicreport'),
    url(r'^communityfromMissionReport/', views.communityfromEngagementReport, name='communityfromEngagementReport'),
    url(r'^projectsfromEngagementReport/', views.projectsfromEngagementReport, name='projectsfromEngagementReport'),
    url(r'^projectsfromCommunityPartnerReport/', views.projectsfromCommunityPartnerReport, name='projectsfromCommunityPartnerReport'),
    path('projectsprivatereport/', views.projectsPrivateReport, name='projectsprivatereport'),
    path('project-private-table-view/',views.projectstablePrivateReport,name='projectprivatetableview'),
    path('communityprivatereport/', views.communityPrivateReport, name='communityprivatereport'),
    path('checkProject/', views.checkProject, name='checkProject'),
    url(r'^saveFocusArea/$',views.saveFocusArea, name='saveFocusArea'),
    url(r'^saveProjectAndRegister/$',views.saveProjectAndRegister, name='saveProjectAndRegister'),
    url(r'^getEngagemetActivityList/$',views.getEngagemetActivityList, name='getEngagemetActivityList'),
    path('myDrafts/', views.myDrafts, name='myDrafts'),
    url(r'^project/(?P<pk>\d+)/delete/$', views.drafts_delete, name='drafts_delete'),
    url('draft-project-done/',views.draft_project_done,name='draft-project-done'),
    url('submit-project-done/', views.submit_project_done, name='submit-project-done'),
    url('adminsubmit_project_done/', views.adminsubmit_project_done, name='adminsubmit_project_done'),


]