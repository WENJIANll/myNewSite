from django.urls import path

from . import views


urlpatterns = [
    path('update_comment', views.update_comment, name='update_comment'),
    path('set_likes/',views.set_likes, name='set_likes'),
]