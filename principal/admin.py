from django.contrib import admin
from .models import Profesor, Clase

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
