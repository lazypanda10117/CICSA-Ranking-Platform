from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='panel.module.management_news.index'),
    path('<str:route>', views.viewDispatch, name='panel.module.management_news.view_dispatch'),
    path('<str:route>/process', views.processDispatch, name='panel.module.management_news.process_dispatch'),
    path('<str:route>/<str:param>', views.viewDispatch, name='panel.module.management_news.view_dispatch_param'),
    path('<str:route>/process/<str:param>', views.processDispatch,
         name='panel.module.management_news.process_dispatch_param'),
]
