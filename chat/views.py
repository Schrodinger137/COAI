from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Q
from plataforma.models import KindUsers, Rol
from principal.models import Clase2
from .models import Message

@login_required
def chat_view(request):
    """Vista principal del chat que redirige según el tipo de usuario"""
    try:
        current_user = KindUsers.objects.get(user=request.user)
        if current_user.kind.filter(rol='profesor').exists():
            return handle_profesor_view(request, current_user)
        return handle_alumno_view(request, current_user)
    except KindUsers.DoesNotExist:
        return render(request, 'chat/no_profesor.html')

def handle_profesor_view(request, current_user):
    """Maneja la vista para profesores"""
    clases_profesor = Clase2.objects.filter(profesor=request.user)
    alumnos = set()
    for clase in clases_profesor:
        alumnos.update(clase.alumnos.all())
    return render(request, 'chat/chat_profesor.html', {'alumnos': alumnos})

def handle_alumno_view(request, current_user):
    """Maneja la vista para alumnos"""
    clase_alumno = Clase2.objects.filter(alumnos=current_user).first()
    if clase_alumno and clase_alumno.profesor:
        profesor = KindUsers.objects.get(user=clase_alumno.profesor)
        return render(request, 'chat/chat_window.html', {
            'profesor': profesor,
            'other_user': profesor.user  # Asegura que other_user esté definido
        })
    return render(request, 'chat/no_profesor.html')

@login_required
def chat_window(request, profesor, alumno):
    profesor_user = get_object_or_404(User, username=profesor)
    alumno_user = get_object_or_404(User, username=alumno)
    
    if request.user not in [profesor_user, alumno_user]:
        return render(request, 'chat/access_denied.html')
    
    # Determina quién es el otro usuario
    if request.user == profesor_user:
        other_user = alumno_user
        other_user_kind = KindUsers.objects.get(user=other_user)
        other_user_name = other_user_kind.user.username  # O usa first_name + last_name si lo prefieres
    else:
        other_user = profesor_user
        other_user_name = "Profesor"  # O puedes usar el nombre real
    
    context = {
        'profesor': profesor_user,
        'alumno': alumno_user,
        'other_user': other_user,
        'other_user_name': other_user_name  # Nuevo campo agregado
    }
    return render(request, 'chat/chat_window.html', context)

@login_required
def send_message(request):
    """Maneja el envío de mensajes"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)
    
    receiver_username = request.POST.get('receiver')
    content = request.POST.get('message')
    
    if not content or not receiver_username:
        return JsonResponse({'status': 'error', 'message': 'Datos incompletos'}, status=400)
    
    try:
        receiver = User.objects.get(username=receiver_username)
        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            content=content
        )
        return JsonResponse({'status': 'ok'})
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Usuario no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
def get_messages(request):
    """Obtiene los mensajes entre dos usuarios con mejor manejo de errores"""
    try:
        print("Solicitud GET recibida:", request.GET)  # Debug
        
        other_user_username = request.GET.get('user')
        if not other_user_username:
            print("Error: Parámetro 'user' faltante")  # Debug
            return JsonResponse({
                'status': 'error',
                'message': 'El parámetro "user" es requerido'
            }, status=400)

        print(f"Buscando usuario: {other_user_username}")  # Debug
        
        other_user = get_object_or_404(User, username=other_user_username)
        
        print(f"Usuario encontrado: {other_user.username}")  # Debug
        
        messages = Message.objects.filter(
            (Q(sender=request.user, receiver=other_user) |
            Q(sender=other_user, receiver=request.user))
        ).order_by('timestamp')
        
        print(f"Mensajes encontrados: {messages.count()}")  # Debug
        
        messages_list = []
        for message in messages:
            messages_list.append({
                'sender': message.sender.username,
                'content': message.content,
                'timestamp': message.timestamp.strftime("%Y-%m-%d %H:%M"),
                'is_sent': message.sender == request.user
            })
        
        return JsonResponse({
            'status': 'ok',
            'messages': messages_list,
            'count': len(messages_list)
        })

    except Exception as e:
        print(f"Error en get_messages: {str(e)}")  # Debug
        return JsonResponse({
            'status': 'error',
            'message': f"Error interno del servidor: {str(e)}"
        }, status=500)