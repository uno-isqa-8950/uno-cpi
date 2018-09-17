from django.urls import path
from . import views


urlpatterns = [
   path('', views.home, name='home'),
   # path('import/', views.importui, name='importui'),
   # path('importcomplete/', views.importcomplete, name='importcomplete'),
   path('upload/', views.upload_csv, name='upload_csv'),
   path('upload_project/', views.upload_project, name='upload_project'),
]
