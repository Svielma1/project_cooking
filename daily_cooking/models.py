from django.db import models

# Create your models here.
class Ingrediente(models.Model):
    id_ingrediente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, help_text="Obligatorio")

    def __str__(self):
        return self.nombre
    
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