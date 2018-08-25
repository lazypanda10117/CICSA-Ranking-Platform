from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='adminIndex'),
    path('search/', include('admin_platform.search.urls'), name='admin.search'),
    #path('data/', include('admin_platform.console.urls'),  name='admin.data_management'),
    path('management/ranking/', include('admin_platform.management.ranking.urls'), name='admin.management.ranking'),
    path('management/event/', include('admin_platform.management.event.urls'), name='admin.management.event'),
]

