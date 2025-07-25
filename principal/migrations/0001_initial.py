# Generated by Django 5.0.6 on 2025-07-13 03:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre Completo del Profesor')),
                ('telefono', models.CharField(blank=True, max_length=20, null=True, verbose_name='# Teléfono')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profesor_profile', to=settings.AUTH_USER_MODEL, verbose_name='Usuario Asociado')),
            ],
            options={
                'verbose_name': 'Profesor',
                'verbose_name_plural': 'Profesores',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Clase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre de la Clase')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción de la Clase')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')),
                ('profesor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='clases_impartidas', to='principal.profesor', verbose_name='Profesor Asignado')),
            ],
            options={
                'verbose_name': 'Clase',
                'verbose_name_plural': 'Clases',
                'ordering': ['-created_at'],
            },
        ),
    ]
