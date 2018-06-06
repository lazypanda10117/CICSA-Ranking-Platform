from django.urls import path

from . import views

urlpatterns = [
    path('/', views.index, name='adminIndex'),
    path('/permission', views.permission, name='adminPermission'),
    path('/login', views.login, name='adminLogin'),
    path('/logout', views.logout, name='adminLogout'),
    path('/event', views.index, name='adminEvent'),
    path('/<str:form_path>/general', views.generalView, name='adminGeneralView'),
    path('/<str:form_path>/generalProcess', views.generalView, name='adminGeneralProcessView'),

]