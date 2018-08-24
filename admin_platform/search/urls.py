from django.urls import path
from .views import SearchView

urlpatterns = [
    path('', SearchView.search, name='adminSearch'),
]