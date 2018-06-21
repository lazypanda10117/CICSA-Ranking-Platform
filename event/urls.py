from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='eventIndex'),
    path('choice', views.choice, name='eventChoice'),
    path('fleet', views.eventAppDispatch, name='eventFleet'),
    path('group', views.eventAppDispatch, name='eventGroup'),
]