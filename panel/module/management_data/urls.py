from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='panel.module.management_data.index'),
    # TODO: integrate prune log into management data
    path('log/prune', views.pruneLog, name='panel.module.management_data.prune_log'),
    path('<str:param>/<str:route>', views.viewDispatch, name='panel.module.management_data.view_dispatch_param'),
]
