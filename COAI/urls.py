"""
URL configuration for COAI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from plataforma import views as plat_views
from principal import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('ejemplo/', plat_views.ejemplo, name='ejemplo'),
    path('clases/', views.clases, name='clases'),
    path('clases/detalles/<int:clase_id>/', views.detalleClase, name='detalleClase'),
    path('profesores/', views.profesores, name='profesores'),
    path('tareas/', views.tareas, name='tareas'),
    path('agregar-tarea/', views.agregar_tarea, name='agregar_tarea'),
]
