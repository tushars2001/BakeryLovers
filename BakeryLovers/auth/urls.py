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
    path('', views.my_account),
    path('create-account/', views.create_account),
    path('reset-password/', views.reset_password),
    path('login/', views.login_user),
    path('account/', views.my_account),
    path('completed-courses/', views.completed_courses),
    path('enrollments/', views.enrollments),
    path('account-update/', views.account_update),
    path('certificate/', views.certificate)
]
