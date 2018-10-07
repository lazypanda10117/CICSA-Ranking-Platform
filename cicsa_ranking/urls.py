from django.urls import include, path

urlpatterns = [
    path('api/', include('api.urls'), name='api'),
    path('panel/', include('panel.urls'), name='panel'),
    path('permission/', include('permission.urls'), name='permission'),
    path('client/', include('client.urls'), name='client')
]
