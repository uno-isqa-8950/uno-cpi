from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf.urls import url
# app_name = 'projects'

urlpatterns = [
    path('communitypartnerproject/', views.communitypartnerproject, name='communitypartnerproject'),
    url(r'^project/(?P<pk>\d+)/edit/$', views.editProject, name='editProject'),
    url(r'^createProject/$', views.createProject, name='createProject'),
    url(r'^projectadd/$', views.project_total_Add, name='projectadd'),
    path('myProjects/',views.myProjects, name='myProjects'),
    path('allProjects/', views.showAllProjects, name='showAllProjects'),
    url(r'^projectSearchAdd/(?P<pk>\d+)/', views.SearchForProjectAdd, name='projectSearchAdd'),
    path('projectspublicreport/', views.projectsPublicReport, name='projectspublicreport'),
    path('communitypublicreport/', views.communityPublicReport, name='communitypublicreport'),
    path('projectsprivatereport/', views.projectsPrivateReport, name='projectsprivatereport'),
    path('communityprivatereport/', views.communityPrivateReport, name='communityprivatereport'),
    path('checkProject/', views.checkProject, name='checkProject'),

]