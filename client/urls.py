from django.urls import path
from . import views

urlpatterns = [
    path('test/<str:param>', views.test, name='client.test'),
]
