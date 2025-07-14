from django.db import models
from django.contrib.auth.models import User # Importamos el modelo User de Django para asociarlo con el profe
from django.utils import timezone
class Profesor(models.Model):
    #vamos a asignar un usuario de django al modelo profesor
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profesor_profile', # Nombre para acceder al perfil desde el objeto User
        verbose_name="Usuario Asociado"
    )
    nombre = models.CharField(max_length=100, verbose_name="Nombre Completo del Profesor")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="# Teléfono")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Profesor"
        verbose_name_plural = "Profesores"
        ordering = ["-created_at"]

    def __str__(self):
        #return self.user.get_full_name() or self.user.username 
         return self.nombre

class Clase(models.Model):
    profesor = models.ForeignKey(
        Profesor,
        on_delete=models.SET_NULL,                
        null=True, blank=True,     
        related_name='clases_impartidas',
        verbose_name="Profesor Asignado"
    )
    nombre = models.CharField(max_length=100, verbose_name="Nombre de la Clase")
    descripcion = models.TextField(verbose_name="Descripción de la Clase", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    class Meta:
        verbose_name = "Clase"
        verbose_name_plural = "Clases"
        ordering = ["-created_at"]

    def __str__(self):
        return self.nombre
    
class Alumno(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Alumno")
    nombre_tutor = models.CharField(max_length=100, verbose_name="Nombre del Tutor")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="# Teléfono")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"
        ordering = ["-created_at"]

    def __str__(self):
        return self.nombre