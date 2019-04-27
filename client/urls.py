from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='client.index'),
    path('scoring/<int:id>', views.scoring, name='client.scoring'),
    path('rotation/<int:id>', views.rotation, name='client.rotation'),
    path('events', views.regattas, name='client.regattas'),
    path('schools', views.schools, name='client.schools'),
    path('seasons', views.seasons, name='client.seasons')
]
