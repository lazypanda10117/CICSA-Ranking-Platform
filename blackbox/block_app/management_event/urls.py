from django.urls import path
from blackbox.block_app.management_event.views import ManagementEventView as MEView

urlpatterns = [
    path('', MEView.home, name='blackbox.block_app.management_event.index'),
    path('<str:dispatch_path>', MEView.viewDispatch, name='blackbox.block_app.management_event.view_dispatch'),
    path('<str:dispatch_path>/process', MEView.processDispatch, name='blackbox.block_app.management_event.process_dispatch'),
    path('<str:dispatch_path>/<str:param>', MEView.viewDispatch, name='blackbox.block_app.management_event.view_dispatch_param'),
    path('<str:dispatch_path>/process/<str:param>', MEView.processDispatch, name='blackbox.block_app.management_event.process_dispatch_param'),
]