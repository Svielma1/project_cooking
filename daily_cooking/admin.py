from django.contrib import admin
from .models import Receta, Ingrediente, RecetaIngrediente, IngredientesUsuario, RestriccionesUsuario

# Register your models here.

admin.site.register(Receta)
admin.site.register(Ingrediente)
admin.site.register(RecetaIngrediente)
admin.site.register(IngredientesUsuario)
admin.site.register(RestriccionesUsuario)
