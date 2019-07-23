from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='panel.core.data_app.index'),
    path('<str:route>', views.viewDispatch, name='panel.core.data_app.view_dispatch'),
    path('<str:route>/process', views.processDispatch, name='panel.core.data_app.process_dispatch'),
    path('<str:route>/<str:param>', views.viewDispatch, name='panel.core.data_app.view_dispatch_param'),
    path('<str:route>/process/<str:param>', views.processDispatch,
         name='panel.core.data_app.process_dispatch_param'),
]
