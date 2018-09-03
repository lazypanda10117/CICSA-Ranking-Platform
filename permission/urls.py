from django.urls import path
from . import views

urlpatterns = [
    path('<str:route>', views.dispatch, name='permission.dispatch'),
]