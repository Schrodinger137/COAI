from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'plataforma/index.html')

def ejemplo(request):
     return render(request, 'plataforma/ejemplo.html')