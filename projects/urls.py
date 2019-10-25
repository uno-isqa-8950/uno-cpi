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
    url(r'^projectsfromMissionReport/(?P<pk>\d+)/', views.projectsfromMissionReport, name='projectsfromMissionReport'),
    url(r'^communityfromMissionReport/(?P<pk>\d+)/', views.communityfromMissionReport, name='communityfromMissionReport'),
    path('communitypublicreport/', views.communityPublicReport, name='communitypublicreport'),
    url(r'^communityfromMissionReport/', views.communityfromEngagementReport, name='communityfromEngagementReport'),
    url(r'^projectsfromEngagementReport/', views.projectsfromEngagementReport, name='projectsfromEngagementReport'),
    path('projectsprivatereport/', views.projectsPrivateReport, name='projectsprivatereport'),
    path('communityprivatereport/', views.communityPrivateReport, name='communityprivatereport'),
    path('checkProject/', views.checkProject, name='checkProject'),
    path('myDrafts/', views.myDrafts, name='myDrafts'),


]