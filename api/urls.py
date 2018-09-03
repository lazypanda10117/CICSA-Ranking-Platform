from django.urls import include, path
from . import views

urlpatterns = [
    path('functional/search', views.search, name='api.search'),
]
