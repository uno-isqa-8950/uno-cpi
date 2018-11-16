from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'account'


urlpatterns = [
    # post_views

    path('loginPage/', views.user_login, name='loginPage'),


]