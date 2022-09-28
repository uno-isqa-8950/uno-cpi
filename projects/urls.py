from django.urls import path, re_path
from django.conf.urls.static import static
from . import views
# app_name = 'projects'

urlpatterns = [
    path('communitypartnerproject/', views.communitypartnerproject, name='communitypartnerproject'),
    re_path(r'^project/(?P<pk>\d+)/edit/$', views.editProject, name='editProject'),
    re_path(r'^create-Project/$', views.createProject, name='createProject'),
    re_path(r'^SuggestProject/$', views.ajax_load_project, name='ajax_load_project'),
    # path('SuggestProject/', views.ajax_load_project, name='ajax_load_project'),
    re_path(r'^projectadd/$', views.project_total_Add, name='projectadd'),
    path('myProjects/',views.myProjects, name='myProjects'),
    path('allProjects/', views.showAllProjects, name='showAllProjects'),
    re_path(r'^projectSearchAdd/(?P<pk>\d+)/', views.SearchForProjectAdd, name='projectSearchAdd'),
    path('projectspublicreport/', views.projectsPublicReport, name='projectspublicreport'),
    path('projectspublictableview/',views.projectstablePublicReport,name='projectspublictableview'),
    path('community-public-report/', views.communityPublicReport, name='communitypublicreport'),
    path('projectsprivatereport/', views.projectsPrivateReport, name='projectsprivatereport'),
    path('project-private-table-view/',views.projectstablePrivateReport,name='projectprivatetableview'),
    path('community-private-report/', views.communityPrivateReport, name='communityprivatereport'),
    path('check-Project/', views.checkProject, name='checkProject'),
    re_path(r'^saveFocusArea/$',views.saveFocusArea, name='saveFocusArea'),
    re_path(r'^saveProjectAndRegister/$',views.saveProjectAndRegister, name='saveProjectAndRegister'),
    re_path(r'^getEngagemetActivityList/$',views.getEngagemetActivityList, name='getEngagemetActivityList'),
    path('myDrafts/', views.myDrafts, name='myDrafts'),
    re_path(r'^project/(?P<pk>\d+)/delete/$', views.drafts_delete, name='drafts_delete'),
    re_path('draft-project-done/',views.draft_project_done,name='draft-project-done'),
    re_path('submit-project-done/', views.submit_project_done, name='submit-project-done'),
    re_path('adminsubmit_project_done/', views.adminsubmit_project_done, name='adminsubmit_project_done'),


]