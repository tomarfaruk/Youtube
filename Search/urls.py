from django.urls import path, include
from . import views
from rest_framework import routers

routs = routers.DefaultRouter()
routs.register('videos', views.VideoView)
urlpatterns = [
    path('', views.index, name='index'),
    path('', include(routs.urls), name='videos')
]
