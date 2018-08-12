from django.urls import path
from blackbox.block_app.management_ranking.views import ManagementRankingView as MRView

urlpatterns = [
    path('', MRView.index, name='managementIndex'),
    path('<str:dispatch_path>', MRView.viewDispatch, name='blackbox.block_app.management_ranking.view_dispatch'),
    path('<str:dispatch_path>/<str:param>', MRView.viewDispatch, name='blackbox.block_app.management_ranking.view_dispatch_param'),
    path('<str:dispatch_path>/process', MRView.processDispatch, name='blackbox.block_app.management_ranking.process_dispatch'),
    path('<str:dispatch_path>/process/<str:param>', MRView.processDispatch, name='blackbox.block_app.management_ranking.process_dispatch_param'),
]