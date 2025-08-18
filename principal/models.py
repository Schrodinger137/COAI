from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 
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

class Duda(models.Model):
    tarea = models.ForeignKey(Tareas, on_delete=models.CASCADE, related_name='dudas')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Duda de {self.autor.username} sobre {self.tarea.titulo}'

class Entrega(models.Model):
    tarea = models.ForeignKey(
        Tareas,
        on_delete=models.CASCADE,
        related_name="entregas",
        verbose_name="Tarea"
    )
    alumno = models.ForeignKey(
        'plataforma.KindUsers',
        on_delete=models.CASCADE,
        related_name="entregas",
        verbose_name="Alumno"
    )
    archivo = models.FileField(upload_to="entregas", verbose_name="Archivo de entrega")
    comentario = models.TextField(blank=True, null=True, verbose_name="Comentario del alumno")
    fecha_entrega = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de entrega")
    calificacion = models.IntegerField(null=True, blank=True, verbose_name="Calificación")

    class Meta:
        verbose_name = "Entrega"
        verbose_name_plural = "Entregas"
        ordering = ["-fecha_entrega"]
        unique_together = ('tarea', 'alumno')  # Cada alumno solo puede entregar una vez

    def __str__(self):
        return f"{self.alumno} - {self.tarea.titulo}"