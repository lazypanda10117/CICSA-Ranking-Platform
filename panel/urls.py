from django.urls import include, path

from panel.module.ModuleRegistry import ModuleRegistryName
from . import views

urlpatterns = [path('', views.index, name='panel.index')] + [
        path('{}/'.format(path), include('panel.module.management_{}.urls'.format(path)))
        for path in ModuleRegistryName().__getAppList__()
    ]

