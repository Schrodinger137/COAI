from django.db import models
from django.contrib.auth.models import User

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
         