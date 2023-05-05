"""UnoCPI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from account import views
from django.contrib.auth import views as auth_views
from account.forms import EmailValidationOnForgotPassword

from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.core import urls as wagtail_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/login/', views.user_login, name = 'adminlogin'),
    path('', include('home.urls')),
    path('partners/', include('partners.urls')),
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=EmailValidationOnForgotPassword), name='password_reset'),
    path('', include('django.contrib.auth.urls')),
    path('account/', include('account.urls')),
    path('', include('projects.urls')),
    re_path(r'^cms/', include(wagtailadmin_urls)),
    re_path(r'^documents/', include(wagtaildocs_urls)),
    re_path(r'^pages/', include(wagtail_urls)),
    re_path(r'', include(wagtail_urls)),
    path(r'session_security/', include('session_security.urls')),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
