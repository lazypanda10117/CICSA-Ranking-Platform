from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='blackbox.block_app.management.ranking.index'),
    path('<str:route>', views.viewDispatch, name='blackbox.block_app.management_ranking.view_dispatch'),
    path('<str:route>/<str:param>', views.viewDispatch, name='blackbox.block_app.management_ranking.view_dispatch_param'),
    path('<str:route>/process', views.processDispatch, name='blackbox.block_app.management_ranking.process_dispatch'),
    path('<str:route>/process/<str:param>', views.processDispatch, name='blackbox.block_app.management_ranking.process_dispatch_param'),
]