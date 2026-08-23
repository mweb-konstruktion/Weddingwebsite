from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.site_login, name='site_login'),
    path('anmeldung/', views.rsvp, name='rsvp'),
    path('', views.home, name='home'),
]
