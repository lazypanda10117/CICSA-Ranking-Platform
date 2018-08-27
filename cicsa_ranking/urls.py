from django.urls import include, path

urlpatterns = [
    path('panel/', include('panel.urls'), name='panel'),
    path('permission/', include('permission.urls'), name='permission'),
]
