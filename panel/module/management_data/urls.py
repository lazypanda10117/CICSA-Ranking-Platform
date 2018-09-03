from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='panel.module.management_data.index'),
    path('<str:param>/<str:route>', views.viewDispatch, name='panel.module.management_data.view_dispatch_param'),
]
