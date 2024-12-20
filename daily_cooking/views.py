from django.shortcuts import render
from .models import Receta

# Create your views here.
def index (request):
    recetas = Receta.objects.all().prefetch_related('receta_ingredientes__ingrediente')
    context = {
        'recetas': recetas
    }
    return render(request, 'index.html', {'recetas': recetas})