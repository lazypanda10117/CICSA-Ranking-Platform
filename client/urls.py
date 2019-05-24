from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='client.index'),
    path('<str:route>', views.viewDispatch, name='client.view_dispatch'),
    path('<str:route>/process', views.processDispatch, name='client.process_dispatch'),
    path('<str:route>/<str:param>', views.viewDispatch, name='client.view_dispatch_param'),
    path('<str:route>/process/<str:param>', views.processDispatch,
         name='client.process_dispatch_param'),
]
