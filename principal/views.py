from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import ProfesorRegistrationForm,ClaseForm
from .models import Profesor, Clase

# Create your views here.


def index(request):
    return render(request, 'principal/index.html')


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('index')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
            return redirect('index')

    return render(request, 'principal/index.html')

def log_out(request):
    logout(request)
    return redirect('index')


def profesores(request):
    form = ProfesorRegistrationForm()
    if request.method == 'POST':
        form = ProfesorRegistrationForm(request.POST)
        if form.is_valid():
            profesor = form.save()#crear el profe, asignarlo al user
            #corrobora si hay un grupo profesores, si no crearlo
            profesores_group, created = Group.objects.get_or_create(name='Profesores')
            if created:
                messages.info(request, "se ha creado el grupo profesores")
            profesor.user.groups.add(profesores_group)
            messages.success(request, f'El profesor {profesor.nombre} ha sido registrado exitosamente.')
            return redirect('profesores')
        else:
            messages.error(request, 'Hubo un error al registrar el profesor. Por favor, revisa los datos en el formulario.')
    lista_profesores = Profesor.objects.all().order_by('-created_at')
    context = {
        'form': form,
        'profesores': lista_profesores,
    }
    return render(request, 'principal/profesores.html', context)

def tareas(request):
    return render(request, 'principal/vistaTareas.html')

def detalleClase(request, clase_id):
    clase = get_object_or_404(Clase, id=clase_id)
    return render(request, 'principal/detalleClase.html', {'clase': clase})

@login_required
def clases(request):
    clases = Clase.objects.all()
    form = ClaseForm()

    if request.method == 'POST':
        form = ClaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Clase registrada')
            return redirect('clases') # Redirige el modal a la misma vista
        else:
            messages.error(request, 'Error al registrar la clase')

    context = {
        'clases': clases,
        'form': form, #pasamos el form al contexto
    }
    return render(request, 'principal/clases.html', context)

def agregar_tarea(request):
    return render(request, 'principal/agregarTarea.html')

