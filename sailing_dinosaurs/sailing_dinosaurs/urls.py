from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('/', include('ranking.urls')),
    path('console/admin/', include('admin_console.urls')),
    path('console/team/', include('team_console.urls')),
    path('admin/', admin.site.urls),
]
