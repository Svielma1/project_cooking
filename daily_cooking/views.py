from .models import Receta, Ingrediente, RecetaIngrediente
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import IngredienteForm, RecetaForm, RecetaIngredienteFormSet
from django.http import HttpResponse
from django.contrib.auth import logout
from .models import IngredientesUsuario
from .forms import RestriccionesForm
from .models import RestriccionesUsuario

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
            return redirect('index')  # Redirige a la vista "inicio" después de iniciar sesión
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'login.html')

def inicio(request):
    return render(request, 'inicio.html')  # Renderiza la plantilla "inicio.html"

def ingresar_ingredientes(request):
    # Obtén o crea el registro de ingredientes del usuario
    ingredientes_usuario, created = IngredientesUsuario.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            # Obtener el nuevo ingrediente del formulario
            nuevo_ingrediente = form.cleaned_data['nombre']

            # Agregar el ingrediente al arreglo si no excede el límite de 5
            if len(ingredientes_usuario.ingredientes) < 5:
                ingredientes_usuario.ingredientes.append(nuevo_ingrediente)
                ingredientes_usuario.save()
            else:
                form.add_error(None, "No puedes agregar más de 5 ingredientes.")
    else:
        form = IngredienteForm()

    context = {
        'form': form,
        'ingredientes': ingredientes_usuario.ingredientes
    }
    return render(request, 'ingresar_ingredientes.html', context)

def ingresar_restricciones(request):
    # Obtén o crea el registro de restricciones del usuario
    restricciones_usuario, created = RestriccionesUsuario.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = RestriccionesForm(request.POST)
        if form.is_valid():
            # Obtener la nueva restricción del formulario
            nueva_restriccion = form.cleaned_data['restriccion']

            # Agregar la restricción al arreglo si no excede el límite de 5
            if len(restricciones_usuario.restricciones) < 5:
                restricciones_usuario.restricciones.append(nueva_restriccion)
                restricciones_usuario.save()
            else:
                form.add_error(None, "No puedes agregar más de 5 restricciones.")

    else:
        form = RestriccionesForm()

    context = {
        'form': form,
        'restricciones': restricciones_usuario.restricciones
    }
    return render(request, 'restricciones.html', context)

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

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('index')