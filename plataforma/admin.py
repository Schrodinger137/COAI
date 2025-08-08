from django.contrib import admin
from .models import *

@admin.register(Rol)
class AdminRol(admin.ModelAdmin):
    list_display = ('id', 'rol')

@admin.register(KindUsers)
class AdminKindUser(admin.ModelAdmin):
    list_display = ('id', 'user', 'get_kinds')
    def get_kinds(self, obj):
        return ", ".join([rol.rol for rol in obj.kind.all()])
    
    get_kinds.short_description = 'Roles'
