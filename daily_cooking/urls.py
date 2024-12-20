"""
URL configuration for project_cooking project.

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
from . import views

urlpatterns = [
    path('', views.index, name='index'),    
    path('login/', views.user_login, name='login'),            # Ruta de login
    path('inicio/', views.inicio, name='inicio'), 
    path('registro/', views.registro, name='registro'),            # Ruta para la vista "inicio"
    path('ingresar-ingredientes/', views.ingresar_ingredientes, name='ingresar_ingredientes'),  # Ruta para ingresar ingredientes
    path('ingresar-restricciones/', views.ingresar_restricciones, name='ingresar_restricciones'),  # Nueva ruta para restricciones
]
