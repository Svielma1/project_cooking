from .models import Receta, Ingrediente, RecetaIngrediente
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import IngredienteForm, RecetaForm, RecetaIngredienteFormSet, RegistroForm
from django.http import HttpResponse
from django.contrib.auth import logout
from .models import IngredientesUsuario
from .forms import RestriccionesForm
from .models import RestriccionesUsuario
from django.core.exceptions import PermissionDenied
# Create your views here.
def index(request):
    # Verificar si el usuario pertenece al grupo "ADMIN"
    es_admin = request.user.groups.filter(name="ADMIN").exists()

    # Obtener las recetas
    recetas = Receta.objects.all().prefetch_related('receta_ingredientes__ingrediente')

    # Pasar las recetas y la variable es_admin al contexto
    context = {
        'recetas': recetas,
        'es_admin': es_admin  # Agregar la variable es_admin
    }

    return render(request, 'index.html', context)
def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Crear el usuario
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Usuario registrado exitosamente. Ahora puedes iniciar sesión.")
            return redirect('login')  # Redirige a la página de inicio de sesión
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {'form': form})

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

@login_required
def agregar_receta(request):
    # Verificar si el usuario pertenece al grupo "ADMIN"
    es_admin = request.user.groups.filter(name="ADMIN").exists()
    
    # Si el usuario no pertenece al grupo "ADMIN", denegar acceso a esta vista
    if not es_admin:
        raise PermissionDenied("No tienes permiso para acceder a esta página.")

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
            return redirect('index')  # Redirige a la página principal (index)
    else:
        receta_form = RecetaForm()
        formset = RecetaIngredienteFormSet()

    context = {
        'receta_form': receta_form,
        'formset': formset,
        'es_admin': es_admin,  # Indicador para mostrar el botón en el template
    }
    return render(request, 'agregar_receta.html', context)

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('index')