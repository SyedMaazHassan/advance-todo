# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('toggle-task', views.toggle_task, name="toggle-task"),
    path('create-task', views.create_task, name="create-task"),
    path('create-child-task', views.create_child_task, name="create-child-task"),
    path('update-priority', views.update_priority, name="update-priority"),
    
    re_path(r'^.*\.*', views.pages, name='pages'),
]
