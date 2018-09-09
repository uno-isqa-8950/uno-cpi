from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from . import views
app_name ='home'

urlpatterns = [
   url(r'^$', views.home, name='home'),
   url(r'^home/$', views.home, name='home'),
]