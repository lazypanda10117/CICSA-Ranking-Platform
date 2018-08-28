from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='panel.management_data.index'),
    path('<str:route>', views.viewDispatch, name='panel.module.management_data.view_dispatch'),
    path('<str:route>/<str:param>', views.viewDispatch, name='panel.module.management_data.view_dispatch_param'),
]
