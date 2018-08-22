from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='adminIndex'),
    path('search/', include('admin_platform.search.urls'), name='adminSearch'),
    path('data/', include('admin_platform.console.urls'),  name='adminDataManagement'),
    path('management/ranking/', include('admin_platform.management.ranking.urls'), name='adminRankingManagement'),
    path('management/event/', include('admin_platform.management.ranking.urls'), name='adminEventManagement'),
]

