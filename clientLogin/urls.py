
from django.contrib import admin
from django.urls import path
import clientLogin.views

urlpatterns = [
    path('index/',clientLogin.views.index),
    path('login/',clientLogin.views.login),
    path('home/',clientLogin.views.home),
    path('signOut/',clientLogin.views.signOut),

    # path('test/',clientLogin.views.test)
]
