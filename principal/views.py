from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import *
from .models import Profesor, Clase, Alumnos, Tareas
from plataforma.models import *

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

@login_required
def profesores(request):
    if request.method == 'POST':
        form = ProfesorRegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            correo = form.cleaned_data['correo']
            password = form.cleaned_data['password']

            # Crear User
            user = User.objects.create_user(
                username=username,
                email=correo,
                password=password
            )

            # Crear KindUser
            kind_user = KindUsers.objects.create(
                user=user,
                tel=form.cleaned_data.get('telefono', '')
            )

            # Asignar rol profesor
            rol_profesor, created = Rol.objects.get_or_create(rol='profesor')
            kind_user.kind.add(rol_profesor)

            messages.success(request, f'El profesor {username} ha sido registrado correctamente.')
            return redirect('profesores')
        else:
            messages.error(request, 'Error al registrar el profesor.')
    else:
        form = ProfesorRegistroForm()

    lista_profesores = KindUsers.objects.filter(kind__rol='profesor')
    context = {
        'form': form,
        'profesores': lista_profesores,
    }
    return render(request, 'principal/profesores.html', context)


def tareas(request):
    tareas = Tareas.objects.all().order_by('-created_at')
    return render(request, 'principal/vistaTareas.html', {'tareas': tareas})

def detalleTarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)
    context = {
        'tarea': tarea,
    }
    return render(request, 'principal/detallesTarea.html', context)

def detalleClase(request, clase_id):
    current_user = KindUsers.objects.filter(user=request.user).first()
    if current_user:
        is_profesor = current_user.kind.filter(rol='profesor').exists()
    else:
        is_profesor = False
    clase = get_object_or_404(Clase2, id=clase_id)
    tareas = Tareas.objects.filter(clase=clase)
    alumnos = clase.alumnos.all()
    form = AlumnoRegistroForm()
    context = {
        'clase':clase,
        'tareas': tareas,
        'alumnos':alumnos,
        'form':form,
        'is_profesor':is_profesor,
    }
    return render(request, 'principal/detalleClase.html', context)

@login_required
def clases(request):
    clases = Clase2.objects.all()
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
    clases = Clase.objects.all()
    if request.method == 'POST':
        form = TareasForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tarea registrada exitosamente.')
            return redirect('tareas')
        else:
            messages.error(request, 'Error al registrar la tarea. Por favor, revisa los datos en el formulario.')

    form = TareasForm()
    return render(request, 'principal/agregarTarea.html', {'form': form, 'clases': clases})


def registroAlumnos(request, clase_id):
    clase = get_object_or_404(Clase2, id=clase_id)

    if request.method == 'POST':
        form = AlumnoRegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            correo = form.cleaned_data['correo']
            password = form.cleaned_data['password']

            user = User.objects.create_user(username=username, email=correo, password=password)
            kind_user = KindUsers.objects.create(user=user, tel=form.cleaned_data.get('telefono', ''))
            rol_alumno, created = Rol.objects.get_or_create(rol='alumno')
            kind_user.kind.add(rol_alumno)
            clase.alumnos.add(kind_user)

            messages.success(request, 'Alumno registrado correctamente')
            return redirect('detalleClase', clase_id=clase.id)
        else:
            messages.error(request, 'Error al registrar el alumno')

    else:
        form = AlumnoRegistroForm()

    return render(request, 'principal/detalleClase.html', {'form': form, 'clase': clase})

def entregas(request):
    return render(request, 'principal/entregasTareas.html')    


def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)
    
    if request.method == 'POST':
        tarea.delete()
        messages.success(request, 'Tarea eliminada exitosamente.')
        return redirect('tareas')
    
    context = {
        'tarea': tarea,
    }
    return render(request, 'principal/eliminarTarea.html', context)