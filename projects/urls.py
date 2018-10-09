from django.urls import path
from django.conf.urls.static import static
from . import views


urlpatterns = [
    # path('communitypartnerhome/', views.communitypartnerhome, name='communitypartnerhome'),
    path('communitypartnerproject/', views.communitypartnerproject, name='communitypartnerproject'),
    # path('communitypartnerproject_edit/<int:pk>/',views.communitypartnerproject_edit, name='communitypartnerproject_edit'),
    ]