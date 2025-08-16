from django.contrib import admin
from .models import *

@admin.register(Rol)
class AdminRol(admin.ModelAdmin):
    list_display = ('id', 'rol')

@admin.register(KindUsers)
class AdminKindUser(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_kinds', 'tel')

    def get_kinds(self, obj):
        return ", ".join([rol.rol for rol in obj.kind.all()])
    get_kinds.short_description = 'Roles'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            # Filtrar para que solo aparezcan usuarios que NO estén en KindUsers
            kwargs["queryset"] = User.objects.exclude(kind_user__isnull=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
