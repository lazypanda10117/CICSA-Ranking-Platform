from django.urls import include
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='panel.index'),
    path('data/', include('panel.module.management_data.urls')),
    path('event/', include('panel.module.management_event.urls')),
    path('ranking/', include('panel.module.management_ranking.urls')),
    path('news/', include('panel.module.management_news.urls')),
    path('league/', include('panel.module.management_league.urls')),
]

