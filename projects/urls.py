from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf.urls import url
# app_name = 'projects'

urlpatterns = [
    # path('communitypartnerhome/', views.communitypartnerhome, name='communitypartnerhome'),
    path('communitypartnerproject/', views.communitypartnerproject, name='communitypartnerproject'),
    path('communitypartnerproject_edit/<int:pk>/',views.communitypartnerproject_edit, name='communitypartnerproject_edit'),

    #url(r'^project/$', views.project_list, name='project_list'),
    url(r'^project/(?P<pk>\d+)/edit/$', views.project_edit_new, name='project_edit_new'),
    url(r'^project_total_Add/$', views.project_total_Add, name='project_total_Add'),
    #url(r'^campususerproject/$', views.proj_view_user, name='proj_view_user'),
    path('campususerproject/',views.proj_view_user, name='proj_view_user'),
    path('projectSearch/', views.SearchForProject, name='SearchForProject'),

]