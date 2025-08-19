from django.db import models
from django.contrib.auth.models import User
from principal.models import Clase2

class Rol(models.Model):
    rol = models.CharField(max_length=100, null=True, unique=True)

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.rol
    
class KindUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='kind_user')
    kind = models.ManyToManyField(Rol, related_name='users')
    tel = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = "Usuario del sistema"
        verbose_name_plural = "Usuarios del sistema"

    def __str__(self):
        roles = ", ".join([role.rol for role in self.kind.all()])
        return f"{self.user.username} - {roles}"
