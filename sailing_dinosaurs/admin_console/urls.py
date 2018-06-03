from django.urls import path

from . import views

urlpatterns = [
    path('/', views.index, name='index'),
    path('/permission', views.permission, name='permission'),
    path('/login', views.login, name='login'),
    path('/logout', views.logout, name='logout'),
    path('/event', views.index, name='index'),
    path('/school', views.schoolView, name='schoolView'),
    path('/<str:form_path>/general', views.generalView, name='generalView'),
]