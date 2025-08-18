from django import forms
from django.contrib.auth.models import User
from .models import *
from django.forms import ClearableFileInput
from plataforma.models import KindUsers

class ProfesorRegistroForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    correo = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        label="Número de Teléfono",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Contraseña"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Repetir contraseña"
    )
    clase = forms.ModelChoiceField(
        queryset=Clase2.objects.filter(profesor__isnull=True),
        required=False,
        label="Asignar Clase",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya está en uso")
        return username

    def clean_correo(self):
        correo = self.cleaned_data.get("correo")
        if User.objects.filter(email=correo).exists():
            raise forms.ValidationError("El correo ya está registrado")
        return correo

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data


class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase2
        fields = ['nombre', 'descripcion', 'profesor']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la Clase'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción'}),
            'profesor': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'nombre': 'Nombre de la Clase',
            'descripcion': 'Descripción',
            'profesor': 'Profesor Asignado',
        }

    # 🔑 Filtramos solo usuarios con rol "profesor"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        profesores = User.objects.filter(kind_user__kind__rol='profesor')
        self.fields['profesor'].queryset = profesores

class AlumnoRegistroForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    correo = forms.EmailField(
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        label="Número de Teléfono",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Contraseña"
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Repetir contraseña"
    )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("El nombre de usuario ya está en uso")
        return username

    def clean_correo(self):
        correo = self.cleaned_data.get("correo")
        if User.objects.filter(email=correo).exists():
            raise forms.ValidationError("El correo ya está registrado")
        return correo

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return cleaned_data



class CustomClearableFileInput(ClearableFileInput):
    template_with_clear = '<br> <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label> %(clear)s'        

class TareasForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['clase', 'titulo', 'descripcion', 'fecha_entrega', 'archivo']
        widgets = {
            'clase': forms.HiddenInput(),  # Se asigna automáticamente desde la vista
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título de la tarea'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción de la tarea'}),
            'fecha_entrega': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'archivo': CustomClearableFileInput,  # Mantienes tu widget personalizado
        }
        labels = {
            'titulo': 'Título',
            'descripcion': 'Descripción',
            'fecha_entrega': 'Fecha de entrega',
            'archivo': 'Archivo adjunto',
        }


class EntregaForm(forms.ModelForm):
    class Meta:
        model = Entrega
        fields = ['archivo', 'comentario']

class DudaForm(forms.ModelForm):
    class Meta:
        model = Duda
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Escribe tu duda o comentario...'}),
        }
        labels = {
            'contenido': 'Duda',
        }