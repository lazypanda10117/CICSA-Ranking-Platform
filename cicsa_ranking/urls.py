from django.urls import include, path

urlpatterns = [
    path('', include('client.urls'), name='client'),
    path('api/', include('api.urls'), name='api'),
    path('panel/', include('panel.urls'), name='panel'),
    path('permission/', include('permission.urls'), name='permission'),
]
