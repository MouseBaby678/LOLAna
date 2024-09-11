"""
URL configuration for LoLAna project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from Analysis import views

urlpatterns = [


    path('admin/', admin.site.urls),
    path("", views.index,name='index'),
    path('aram/', views.aram, name='aram'),
    path('arena/', views.arena, name='arena'),
    path('bestteam_aram/', views.bestteam_aram, name='bestteam_aram'),
    path('bestteam_arena/', views.bestteam_arena, name='bestteam_arena'),
    path('bestteam_normal/', views.bestteam_normal, name='bestteam_normal'),
    path('bottom/', views.bottom, name='bottom'),
    path('jungle/', views.jungle, name='jungle'),
    path('middle/', views.middle, name='middle'),
    path('ranked_flex/', views.ranked_flex, name='ranked_flex'),
    path('ranked_solo/', views.ranked_solo, name='ranked_solo'),
    path('support/', views.support, name='support'),
    path('top/', views.top, name='top'),
    path('analysis/', views.analysis, name='analysis'),
    path('analysis_hero/', views.analysis_hero, name='analysis_hero')
    # path("hero_list/", views.List.as_view()),

]
