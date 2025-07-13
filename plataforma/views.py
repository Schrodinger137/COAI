from django.shortcuts import render

# Create your views here.

def ejemplo(request):
     return render(request, 'plataforma/ejemplo.html')