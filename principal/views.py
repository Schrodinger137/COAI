from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import ProfesorRegistrationForm,ClaseForm, AlumnosForm, TareasForm
from .models import Profesor, Clase, Alumnos, Tareas
from plataforma.models import KindUsers

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

    form = ProfesorRegistrationForm()
    if request.method == 'POST':
        form = ProfesorRegistrationForm(request.POST)
        if form.is_valid():
            profesor = form.save()
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
    clase = get_object_or_404(Clase, id=clase_id)
    alumnos = Alumnos.objects.filter(clase=clase)
    tareas = Tareas.objects.filter(clase=clase)
    context = {
        'clase':clase,
        'alumnos': alumnos,
        'tareas': tareas,
        'is_profesor':is_profesor,
    }
    return render(request, 'principal/detalleClase.html', context)

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
    
    clase = get_object_or_404(Clase, id=clase_id)

    if request.method == 'POST':
        form = AlumnosForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)
            alumno.clase = clase  # asigna la clase seleccionada
            alumno.save()
            messages.success(request, 'Alumno registrado')
            return redirect('detalleClase', clase_id=clase.id)

    form = AlumnosForm()
    return render(request, 'principal/detalleClase.html', {'form': form, 'clase': clase})


    