from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'


urlpatterns = [
    # post_views

    path('login-Page/', views.user_login, name='loginPage'),
    path('', views.index),
    path('attrs/', views.attrs),
    path('metadata/', views.metadata)

]