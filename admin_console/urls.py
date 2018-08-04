from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='adminIndex'),
    path('permission', views.permission, name='adminPermission'),
    path('login', views.login, name='adminLogin'),
    path('logout', views.logout, name='adminLogout'),
    path('search', views.search, name='adminSearch'),
    path('<str:form_path>/general', views.generalView, name='adminGeneralView'),
    path('<str:form_path>/generalProcess', views.generalView, name='adminGeneralProcessView'),
    path('<str:form_path>/custom', views.customView, name='adminCustomView'),
    path('<str:form_path>/customProcess', views.customView, name='adminCustomProcessView'),
    path('management/ranking/', include('ranking_management.urls'), name='adminRankingManagement'),
    path('management/event/', include('event_management.urls'), name='adminEventManagement'),
]