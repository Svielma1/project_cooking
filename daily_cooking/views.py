from .models import Receta
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
def index (request):
    recetas = Receta.objects.all().prefetch_related('receta_ingredientes__ingrediente')
    context = {
        'recetas': recetas
    }
    return render(request, 'index.html', {'recetas': recetas})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')  # Redirige a la vista "inicio" después de iniciar sesión
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

def inicio(request):
    return render(request, 'inicio.html')  # Renderiza la plantilla "inicio.html"

def ingresar_ingredientes(request):
    return render(request, 'ingresar_ingredientes.html')  # Página para ingresar ingredientes

def ingresar_restricciones(request):
    return render(request, 'restricciones.html')  # Redirige a una plantilla de restricciones
