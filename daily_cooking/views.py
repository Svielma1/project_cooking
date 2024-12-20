from .models import Receta, Ingrediente, RecetaIngrediente
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import IngredienteForm, RecetaForm, RecetaIngredienteFormSet
from django.http import HttpResponse

# Create your views here.
def index (request):
    recetas = Receta.objects.all().prefetch_related('receta_ingredientes__ingrediente')
    context = {
        'recetas': recetas
    }
    return render(request, 'index.html', {'recetas': recetas})

def registro(request):
    if request.method == 'POST':
        # Aquí puedes agregar la lógica para registrar a un usuario, por ejemplo
        pass
    return render(request, 'registro.html')

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
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el ingrediente en la base de datos
            # Redirige a la misma página o a una página de éxito
            return redirect('ingresar_ingredientes')
    else:
        form = IngredienteForm()

    return render(request, 'ingresar_ingredientes.html', {'form': form})

def ingresar_restricciones(request):
    return render(request, 'restricciones.html')  # Redirige a una plantilla de restricciones

def agregar_receta(request):
    if request.method == 'POST':
        receta_form = RecetaForm(request.POST)
        formset = RecetaIngredienteFormSet(request.POST)
        if receta_form.is_valid() and formset.is_valid():
            receta = receta_form.save()
            for form in formset:
                nombre_ingrediente = form.cleaned_data['ingrediente_nombre']
                ingrediente, created = Ingrediente.objects.get_or_create(nombre=nombre_ingrediente)
                cantidad = form.cleaned_data['cantidad']
                RecetaIngrediente.objects.create(receta=receta, ingrediente=ingrediente, cantidad=cantidad)
            return redirect(index)
    else:
        receta_form = RecetaForm()
        formset = RecetaIngredienteFormSet()
    
    context = {
        'receta_form': receta_form,
        'formset': formset
    }
    return render(request, 'agregar_receta.html', context)