from django.urls import path

from . import views

urlpatterns = [
    path('admin/', views.admin, name='admin'),
    path('posts/', views.posts, name='posts'),
    path('comments/', views.comments, name='comments'),
    path('users/<user_id>/posts/', views.userPost, name='userPost'),
]