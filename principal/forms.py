from django import forms
from django.contrib.auth.models import User
from .models import Profesor,Clase, Alumnos, Tareas
from django.forms import ClearableFileInput

class ProfesorRegistrationForm(forms.ModelForm):
    # Campos para el modelo User
    username = forms.CharField(
        max_length=150,
        label="Usuario"
    )
    email = forms.EmailField(
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Contraseña"
    )
    password_confirm = forms.CharField( # Campo para confirmar la contraseña
        widget=forms.PasswordInput,
        label="Confirmar Contraseña",
    )
    first_name = forms.CharField(
        max_length=30,
        required=True, # Hacer el nombre real requerido
        label="Nombre(s)"
    )
    last_name = forms.CharField(
        max_length=30,
        required=True, # Hacer el apellido real requerido
        label="Apellido(s)"
    )
    class Meta:
        model = Profesor
        # establecemos el orden de los campos
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password_confirm',
            'telefono'#telefono es parte del modelo pero no del user, se agrega aqui
        ]
        
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre ya está en uso.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está registrado.")
        return email

    def clean(self):
        # Validar que las contraseñas coincidan
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        # 1. Crear el usuario de Django
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name']
        )
        # Por defecto, un profesor NO es staff ni superusuario
        user.is_staff = False
        user.is_superuser = False
        user.save()

        # Crear la instancia del modelo y agregarla al user
        profesor = super().save(commit=False) # crea la instancia
        profesor.user = user #asigna el usuario creado a la instancia del modelo profesor

        # agregamos first y last name del user al modelo
        profesor.nombre = self.cleaned_data['first_name'] + ' ' + self.cleaned_data['last_name']
        #profesor.nombre = f"{self.cleaned_data['first_name']} {self.cleaned_data['last_name']}"
        if commit:
            profesor.save()

        return profesor
class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
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

class AlumnosForm(forms.ModelForm):
    class Meta:
        model = Alumnos
        fields = ['nombre', 'tutor', 'telefono', 'correo', 'password']


class CustomClearableFileInput(ClearableFileInput):
    template_with_clear = '<br> <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label> %(clear)s'        

class TareasForm(forms.ModelForm):
    class Meta:
        model = Tareas
        fields = ['clase', 'titulo', 'descripcion', 'fecha_entrega', 'archivo']
        widgets={
            'archivo': CustomClearableFileInput
        }
