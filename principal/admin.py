from django.contrib import admin
from .models import Profesor, Clase, Alumnos, Tareas

@admin.register(Profesor)
class ProfesorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'user', 'telefono', 'created_at')
    search_fields = ('nombre', 'user__username', 'user__email')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(Clase)
class ClaseAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'profesor', 'created_at')
    search_fields = ('nombre', 'descripcion', 'profesor__nombre')
    list_filter = ('created_at', 'profesor')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)


class AlumnosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tutor', 'telefono', 'correo', 'clase', 'created_at')
    search_fields = ('nombre', 'tutor', 'correo', 'clase')
    list_filter = ('created_at', 'clase')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)    
admin.site.register(Alumnos, AlumnosAdmin)    

class TareasAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'clase', 'fecha_entrega', 'created_at')
    search_fields = ('titulo', 'descripcion', 'clase__nombre')
    list_filter = ('fecha_entrega', 'clase')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
admin.site.register(Tareas, TareasAdmin)    