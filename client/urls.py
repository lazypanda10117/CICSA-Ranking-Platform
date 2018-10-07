from django.urls import path
from . import views

urlpatterns = [
    path('test/<int:param>', views.test, name='client.test'),
    path('scoring/<int:id>', views.scoring, name='client.scoring')
]
