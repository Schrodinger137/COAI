from django.contrib import admin
from .models import *
from plataforma.models import *

@admin.register(Clase2)
class Clase2Admin(admin.ModelAdmin):
    list_display = ('nombre', 'profesor', 'created_at')
    search_fields = (
        'nombre',
        'descripcion',
        'profesor__username',
        'profesor__first_name',
        'profesor__last_name',
        'alumnos__user__username',
        'alumnos__user__first_name',
        'alumnos__user__last_name',
    )
    filter_horizontal = ('alumnos',)
    list_filter = ('created_at', 'profesor')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "alumnos":
            try:
                rol_alumno = Rol.objects.get(rol__iexact="alumno")
                kwargs["queryset"] = KindUsers.objects.filter(kind=rol_alumno)
            except Rol.DoesNotExist:
                kwargs["queryset"] = KindUsers.objects.none()
        return super().formfield_for_manytomany(db_field, request, **kwargs)

class TareasAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'clase', 'fecha_entrega', 'created_at')
    search_fields = ('titulo', 'descripcion', 'clase__nombre')
    list_filter = ('fecha_entrega', 'clase')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
admin.site.register(Tareas, TareasAdmin)    

@admin.register(Entrega)
class EntregaAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'comentario', 'archivo', 'fecha_entrega')