"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('library/', views.index),

    path('library/<int:library_id>/', views.library, name='library'),

    path('tv_show/<int:tv_show_id>/', views.tv_show, name='tv_show'),

    path('season/<int:tv_season_id>/', views.tv_season, name='tv_season'),

    path('episode/<int:tv_episode_id>/', views.tv_episode, name='tv_episode'),

    path('media_file/<int:media_file_id>/', views.media_file, name='media_file'),

    path('hls_start/<int:media_file_id>', views.hls_start, name='hls_start'),

    path('hls_pause/<int:hls_id>', views.hls_pause, name='hls_pause'),

    path('hls_resume/<int:hls_id>', views.hls_resume, name='hls_resume'),

    path('hls_stop/<int:hls_id>', views.hls_stop, name='hls_stop'),

    path('api/scan/<int:library_id>/', views.scan, name='scan'),
]
