from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf.urls import url
# app_name = 'projects'

urlpatterns = [
    # path('communitypartnerhome/', views.communitypartnerhome, name='communitypartnerhome'),
    path('communitypartnerproject/', views.communitypartnerproject, name='communitypartnerproject'),
    #path('communitypartnerprojectedit/<int:pk>/',views.communitypartnerprojectedit, name='communitypartnerprojectedit'),

    #url(r'^project/$', views.project_list, name='project_list'),
    url(r'^project/(?P<pk>\d+)/edit/$', views.editProject, name='editProject'),
    url(r'^createProject/$', views.createProject, name='createProject'),
    path('myProjects/',views.myProjects, name='myProjects'),
    url(r'^allProjects/', views.showAllProjects, name='showAllProjects'),
    url(r'^projectSearchAdd/(?P<pk>\d+)/', views.SearchForProjectAdd, name='projectSearchAdd'),
    path('projectspublicreport/', views.projectsPublicReport, name='projectspublicreport'),
    path('communitypublicreport/', views.communityPublicReport, name='communitypublicreport'),
    path('projectsprivatereport/', views.projectsPrivateReport, name='projectsprivatereport'),
    path('communityprivatereport/', views.communityPrivateReport, name='communityprivatereport'),

]