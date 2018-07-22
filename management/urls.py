from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='managementIndex'),
    path('events', views.eventList, name='managementEvents'),
    path('event/<str:event_id>', views.specificEvent, name='managementSpecificEvent'),
    path('event/<str:event_id>/update/<str:event_status>', views.updateEventStatus,
         name='managementUpdateEventStatus'),
    path('event activities/<str:event_activity_id>', views.specificEventActivity, name='managementSpecificEventActivity'),
]