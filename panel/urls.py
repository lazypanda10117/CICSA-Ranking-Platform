from django.urls import include, path

from . import views

urlpatterns = [
    path('data/', include('panel.module.management_data.urls')),
    path('event/', include('panel.module.management_event.urls')),
    path('ranking/', include('panel.module.management_ranking.urls')),
]
