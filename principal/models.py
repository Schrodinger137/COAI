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

class Clase2(models.Model):
    profesor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='clases_impartidas',
        verbose_name="Profesor Asignado"
    )
    alumnos = models.ManyToManyField(
        'plataforma.KindUsers',
        related_name='clases_inscritas',
        verbose_name="Alumnos Inscritos",
        blank=True
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    
class Alumnos(models.Model):
    nombre = models.CharField(max_length=100, verbose_name="Nombre del Alumno")
    tutor = models.CharField(max_length=100, verbose_name="Nombre del Tutor")
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Numero de Teléfono")
    correo = models.EmailField(verbose_name="Correo Electrónico")
    password = models.CharField(max_length=128, verbose_name="Contraseña")

    clase = models.ForeignKey(
        Clase,
        on_delete=models.CASCADE,
        verbose_name="Clase Inscrita"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Alumno"
        verbose_name_plural = "Alumnos"
        ordering = ["-created_at"]

    def __str__(self):
        return self.nombre   

class Tareas(models.Model):
    titulo = models.CharField(max_length=100, verbose_name="Título de la Tarea")
    descripcion = models.TextField(verbose_name="Descripción de la Tarea")
    fecha_entrega = models.DateTimeField(verbose_name="Fecha de Entrega")
    clase = models.ForeignKey(
        Clase2,
        on_delete=models.CASCADE,
        verbose_name="Clase Asociada"
    )
    archivo = models.FileField(upload_to="archivos", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        verbose_name = "Tarea"
        verbose_name_plural = "Tareas"
        ordering = ["-created_at"]

    def __str__(self):
        return self.titulo
         