from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='eventManagementIndex'),
    path('<str:dispatch_path>', views.dispatch, name='eventManagementEvents'),
    path('<str:dispatch_path>/<str:element_id>', views.dispatchSpecific, name='eventManagementSpecificObject'),
]