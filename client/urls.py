from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name='client.index'),
    path('scoring/<int:id>', views.scoring, name='client.scoring'),
    path('regattas', views.regattas, name='client.regattas')
]
