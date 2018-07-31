from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='eventManagementIndex'),
    path('choice', views.choice, name='eventManagementChoice'),
    path('<str:type>', views.eventFilter, name='eventManagementEventFilter'),
    path('<str:dispatch_path>/<str:param>', views.viewDispatch, name='eventManagementDispatch'),
]