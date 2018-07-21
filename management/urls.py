from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='managementIndex'),
    path('events', views.eventList, name='managementEvents'),
]