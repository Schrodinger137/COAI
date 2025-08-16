from django.shortcuts import render
from django.http import JsonResponse
from .models import Message
import json

def chat_window(request):
    return render(request, 'chat/chat_window.html')

def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = Message.objects.create(
            user=data['user'],
            content=data['content']
        )
        return JsonResponse({'status': 'success', 'message_id': message.id})

def get_messages(request):
    messages = Message.objects.all().order_by('timestamp')
    messages_list = [{'user': msg.user, 'content': msg.content, 'timestamp': msg.timestamp} for msg in messages]
    return JsonResponse(messages_list, safe=False)