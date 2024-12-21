from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Ingrediente(models.Model):
    id_ingrediente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    def __str__(self):
        return self.nombre
    
class IngredientesUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ingredientes = models.JSONField(default=list, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ingredientes de {self.user.username}"
    
class RestriccionesUsuario(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restricciones = models.JSONField(default=list)  # Arreglo para almacenar las restricciones
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Restricciones de {self.user.username}"
    
class Receta(models.Model):
    id_receta = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, help_text="Obligatorio")
    descripcion = models.TextField()
    metodo = models.TextField()

    def __str__(self):
        return self.nombre

class RecetaIngrediente(models.Model):
    receta = models.ForeignKey(Receta, on_delete=models.CASCADE, related_name='receta_ingredientes')
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    cantidad = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.cantidad} { self.ingrediente.nombre} para {self.receta.nombre}"