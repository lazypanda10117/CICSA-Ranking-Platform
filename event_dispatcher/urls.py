from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='eventIndex'),
    path('choice', views.choice, name='eventChoice'),
    path('<str:event_type>', views.eventAppDispatch, name='eventDispatch'),
]