from django.urls import path
from blackbox.block_app.management_event.views import ManagementEventView as MEView

urlpatterns = [
    path('', MEView.home, name='blackbox.block_app.management_event.index'),
    path('choice', MEView.choice, name='blackbox.block_app.management_event.choice'),
    path('<str:type>', MEView.eventFilter, name='blackbox.block_app.management_event.event_filter'),
    path('<str:dispatch_path>/<str:param>', MEView.viewDispatch, name='blackbox.block_app.management_event.view_dispatch'),
]