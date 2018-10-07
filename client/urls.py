from django.urls import path
from . import views

urlpatterns = [
    path('scoring/<int:id>', views.scoring, name='client.scoring')
]
