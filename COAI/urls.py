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
from chat import views as chat_views
from django.conf import settings

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
    path('clase/<int:clase_id>/agregar-tarea/', views.agregar_tarea, name='agregar_tarea'),
    path('tareas/detalles/<int:tarea_id>/', views.detalleTarea, name='detalleTarea'),
    path('entregar_tarea/<int:tarea_id>/', views.entregar_tarea, name='entregar_tarea'),
    path('entregas', views.entregas, name='entregas'),
    path('registroAlumnos/<int:clase_id>/', views.registroAlumnos , name='registroAlumnos'),
    path('eliminar_tarea/<int:tarea_id>/', views.eliminar_tarea, name='eliminar_tarea'),
    path('chat/', chat_views.chat_window, name='chat_window'),
    path('send_message/', chat_views.send_message, name='send_message'),
    path('get_messages/', chat_views.get_messages, name='get_messages'),
    path('cuenta/', views.cuenta, name='cuenta'),
    
]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    