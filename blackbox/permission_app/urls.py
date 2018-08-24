from django.urls import path
from blackbox.permission_app.views import PermissionView as PView

urlpatterns = [
    path('login', PView.login, name='blackbox.permission_app.login'),
    path('logout', PView.logout, name='blackbox.permission_app.logout'),
]