from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.site_login, name='site_login'),
    path('', views.home, name='home'),
]
