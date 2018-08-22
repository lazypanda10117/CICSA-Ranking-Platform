from django.urls import include, path

urlpatterns = [
    path('platform/admin/', include('admin_platform.urls'), name='adminPlatform'),
    path('platform/team/', include('team_platform.urls'), name='teamPlatform'),
    path('permission/', include('permission_app.urls'), name='permission'),
]
