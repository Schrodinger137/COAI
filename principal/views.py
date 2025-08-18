from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import Group
from .forms import *
from .models import Tareas,Duda
from plataforma.models import *
from functools import wraps

# Create your views here.


def agregar_roles(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        request.current_user = None
        request.is_profesor = False
        request.is_alumno = False

        if request.user.is_authenticated:
            request.current_user = KindUsers.objects.filter(user=request.user).first()
            if request.current_user:
                request.is_profesor = request.current_user.kind.filter(
                    rol="profesor"
                ).exists()
                request.is_alumno = request.current_user.kind.filter(
                    rol="alumno"
                ).exists()

        return view_func(request, *args, **kwargs)

    return wrapper


def index(request):
    return render(request, "principal/index.html")


def log_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Inicio de sesión exitoso.")
            return redirect("index")
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
            return redirect("index")

    return render(request, "principal/index.html")


def log_out(request):
    logout(request)
    return redirect("index")


@login_required
@agregar_roles
def profesores(request):
    form = ProfesorRegistroForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data["username"],
            email=form.cleaned_data["correo"],
            password=form.cleaned_data["password"],
        )
        kind_user = KindUsers.objects.create(
            user=user, tel=form.cleaned_data.get("telefono", "")
        )
        rol_profesor, _ = Rol.objects.get_or_create(rol="profesor")
        kind_user.kind.add(rol_profesor)

        clase_seleccionada = form.cleaned_data.get("clase")
        if clase_seleccionada:
            clase_seleccionada.profesor = user
            clase_seleccionada.save()

        messages.success(
            request, f"El profesor {user.username} ha sido registrado correctamente."
        )
        return redirect("profesores")

    if request.user.is_superuser or request.is_profesor:
        lista_profesores = KindUsers.objects.filter(kind__rol="profesor")
    elif request.is_alumno:
        clases_alumno = Clase2.objects.filter(alumnos=request.current_user)
        lista_profesores = KindUsers.objects.filter(
            kind__rol="profesor",
            user__in=clases_alumno.values_list("profesor", flat=True),
        )
    else:
        lista_profesores = KindUsers.objects.none()

    context = {
        "form": form,
        "profesores": lista_profesores,
        "is_profesor": request.is_profesor,
        "is_alumno": request.is_alumno,
    }

    return render(request, "principal/profesores.html", context)


from django.utils import timezone

@login_required
@agregar_roles
def tareas(request):
    # Obtener el estado del switch (True si está activado)
    mostrar_todas = request.GET.get('mostrar_todas', 'false') == 'true'
    
    # Obtener el usuario actual con su perfil extendido
    current_user = request.current_user
    
    # Base queryset
    if request.is_profesor:
        tareas = Tareas.objects.filter(clase__profesor=request.user)
    elif request.is_alumno:
        tareas = Tareas.objects.filter(clase__alumnos=current_user)
    else:
        tareas = Tareas.objects.all()
    
    # Filtrar por fecha si no se quieren mostrar todas
    if not mostrar_todas:
        tareas = tareas.filter(fecha_entrega__gte=timezone.now())
    
    # Ordenar por fecha de creación
    tareas = tareas.order_by("-created_at")
    
    return render(request, "principal/vistaTareas.html", {
        "tareas": tareas,
        "mostrar_todas": mostrar_todas,
        "now": timezone.now()
    }) 
   


@agregar_roles
@login_required
def agregar_tarea(request, clase_id):
    clase = get_object_or_404(Clase2, id=clase_id)

    # Solo el profesor de la clase o superuser pueden agregar tareas
    if (
        not (request.is_profesor and request.current_user.user == clase.profesor)
        and not request.user.is_superuser
    ):
        messages.error(request, "No tienes permiso para agregar tareas a esta clase.")
        return redirect("detalleClase", clase_id=clase.id)

    if request.method == "POST":
        form = TareasForm(request.POST, request.FILES)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.clase = clase  # Aseguramos que la tarea quede vinculada a la clase
            tarea.save()
            messages.success(request, f"Tarea '{tarea.titulo}' agregada correctamente.")
            return redirect("detalleClase", clase_id=clase.id)
        else:
            messages.error(request, "Error al agregar la tarea. Revisa los datos.")
    else:
        form = TareasForm(initial={"clase": clase})

    context = {
        "form": form,
        "clase": clase,
        "is_profesor": request.is_profesor,
        "is_alumno": request.is_alumno,
    }

    return render(request, "principal/agregarTarea.html", context)


@agregar_roles
@login_required
def detalleTarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)

    # Handle POST requests
    if request.method == 'POST':
        # checa si es el form duda
        if 'duda_form_submit' in request.POST:
            duda_form = DudaForm(request.POST)
            if duda_form.is_valid():
                duda = duda_form.save(commit=False)
                duda.tarea = tarea
                duda.autor = request.user
                duda.save()
                messages.success(request, '¡Tu duda ha sido publicada!')
                return redirect('detalleTarea', tarea_id=tarea.id)
            else:
                messages.error(request, 'Hubo un error al enviar tu duda. Por favor, revisa el formulario.')
        
        # checa si es el form entrega
        elif 'entrega_form_submit' in request.POST:
            entrega_form = EntregaForm(request.POST, request.FILES)
            if entrega_form.is_valid():
                entrega = entrega_form.save(commit=False)
                entrega.tarea = tarea
                entrega.alumno = request.user.kind_user
                entrega.save()
                messages.success(request, '¡Tarea entregada con éxito!')
                return redirect('detalleTarea', tarea_id=tarea.id)
            else:
                messages.error(request, 'Hubo un error al entregar la tarea.')

    dudas = tarea.dudas.all().order_by('-fecha_creacion')
    duda_form = DudaForm()
    entrega_form = EntregaForm()

    context = {
        "tarea": tarea,
        "is_profesor": request.is_profesor,
        "is_alumno": request.is_alumno,
        "entrega_form": entrega_form,
        "duda_form": duda_form,
        "dudas": dudas,
    }
    
    return render(request, "principal/detallesTarea.html", context)

@agregar_roles
@login_required
def detalleClase(request, clase_id):
    clase = get_object_or_404(Clase2, id=clase_id)

    if not (request.is_profesor or request.is_alumno or request.user.is_superuser):
        messages.error(request, "No tienes acceso a esta clase.")
        return redirect("clases")

    if request.is_alumno and request.current_user not in clase.alumnos.all():
        messages.error(request, "No puedes ver esta clase.")
        return redirect("clases")

    tareas = Tareas.objects.filter(clase=clase)
    alumnos = clase.alumnos.all()
    form = AlumnoRegistroForm()
    tareaForm = TareasForm(initial={"clase": clase})

    context = {
        "clase": clase,
        "tareas": tareas,
        "alumnos": alumnos,
        "form": form,
        "tareaForm": tareaForm,
        "is_profesor": request.is_profesor,
        "is_alumno": request.is_alumno,
    }
    return render(request, "principal/detalleClase.html", context)


@login_required
@agregar_roles
def clases(request):
    form = ClaseForm()

    if request.user.is_superuser:
        clases = Clase2.objects.all()
    elif request.is_profesor:
        clases = Clase2.objects.filter(profesor=request.current_user.user)
    elif request.is_alumno:
        clases = Clase2.objects.filter(alumnos=request.current_user)
    else:
        clases = Clase2.objects.none()

    if request.method == "POST":
        form = ClaseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Clase registrada")
            return redirect("clases")
        else:
            messages.error(request, "Error al registrar la clase")

    context = {
        "clases": clases,
        "form": form,
        "is_profesor": request.is_profesor,
        "is_alumno": request.is_alumno,
    }

    return render(request, "principal/clases.html", context)


@login_required
def registroAlumnos(request, clase_id):
    clase = get_object_or_404(Clase2, id=clase_id)

    if request.method == "POST":
        form = AlumnoRegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            correo = form.cleaned_data["correo"]
            password = form.cleaned_data["password"]

            user = User.objects.create_user(
                username=username, email=correo, password=password
            )
            kind_user = KindUsers.objects.create(
                user=user, tel=form.cleaned_data.get("telefono", "")
            )
            rol_alumno, created = Rol.objects.get_or_create(rol="alumno")
            kind_user.kind.add(rol_alumno)
            clase.alumnos.add(kind_user)

            messages.success(request, "Alumno registrado correctamente")
            return redirect("detalleClase", clase_id=clase.id)
        else:
            messages.error(request, "Error al registrar el alumno")

    else:
        form = AlumnoRegistroForm()

    return render(
        request, "principal/detalleClase.html", {"form": form, "clase": clase}
    )


@login_required
def entregas(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)
    entregas = Entrega.objects.filter(tarea=tarea)  # solo entregas de esa tarea
    return render(request, "principal/entregasTareas.html", {
        "tarea": tarea,
        "entregas": entregas
    })


@login_required
def entregar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)
    alumno = KindUsers.objects.filter(user=request.user).first()

    if request.method == "POST":
        form = EntregaForm(request.POST, request.FILES)
        if form.is_valid():
            entrega, created = Entrega.objects.update_or_create(
                tarea=tarea,
                alumno=alumno,
                defaults={
                    "archivo": form.cleaned_data["archivo"],
                    "comentario": form.cleaned_data.get("comentario", ""),
                },
            )
            messages.success(request, "Tu entrega se ha registrado correctamente.")
            return redirect("detalleTarea", tarea_id=tarea.id)
        else:
            messages.error(
                request, "Error al subir la entrega. Revisa los datos ingresados."
            )
    else:
        form = EntregaForm()

    context = {
        "tarea": tarea,
        "form": form,
    }
    return render(request, "principal/detallesTarea.html", context)


@login_required
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tareas, id=tarea_id)

    if request.method == "POST":
        tarea.delete()
        messages.success(request, "Tarea eliminada exitosamente.")
        return redirect("tareas")

    context = {
        "tarea": tarea,
    }

    return render(request, 'principal/eliminarTarea.html', context)

@login_required
@agregar_roles
def cuenta(request):
    # Asegúrate de pasar current_user al contexto
    return render(request, 'principal/edicionPerfil.html', {
        'user': request.user,
        'current_user': request.current_user
    })


def calificarTarea(request, entrega_id):
    entrega = get_object_or_404(Entrega, id=entrega_id)

    if request.method == "POST":
        calificacion = request.POST.get("calificacion")
        if calificacion.isdigit():
            entrega.calificacion = int(calificacion)
            entrega.save()
            messages.success(request, "Calificación registrada correctamente.")
        else:
            messages.error(request, "La calificación debe ser un número entero.")

    return redirect("entregas", tarea_id=entrega.tarea.id)

@login_required
@agregar_roles
def editar_perfil(request):
    if request.method == 'POST':
        # Actualizar datos del User
        user = request.user
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email')
        
        # Actualizar contraseña si se proporcionó
        password = request.POST.get('password')
        if password:
            user.set_password(password)
        
        user.save()
        
        if hasattr(request, 'current_user') and request.current_user:
            request.current_user.tel = request.POST.get('telefono', '')
            request.current_user.save()
        
        messages.success(request, 'Perfil actualizado correctamente')
        return redirect('/')
    
    return redirect('/')
