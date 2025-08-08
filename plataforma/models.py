from django.db import models
from django.contrib.auth.models import User

class Rol(models.Model):
    rol = models.CharField(max_length=100, null=True, unique=True)

    def __str__(self):
        return self.rol
class KindUsers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='kind_user')
    kind = models.ManyToManyField(Rol, related_name='users')
    tel = models.IntegerField(null=True)

    def __str__(self):
        roles = ", ".join([role.rol for role in self.kind.all()])
        return f"{self.user.username} - {roles}"
    

    
    