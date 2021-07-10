"""BakeryLovers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.home),
    path('create-session/', views.create_session),
    path('view-sessions/', views.view_sessions),
    path('create-account/', views.create_account),
    path('view-accounts/', views.view_accounts),
    path('select-session/', views.select_session),
    path('select-session/assign-students/', views.assign_students),
    path('select-session/assign-students/session-students/', views.session_students),
    path('view-session-students/', views.view_session_students),
]
