from django import forms
from .models import Ingrediente, Receta, RecetaIngrediente

class IngredienteForm(forms.Form):
    nombre = forms.CharField(
        max_length=100,
        label="Nombre del Ingrediente",
        widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: Tomate'})
    )

class RecetaForm(forms.ModelForm):
    class Meta:
        model = Receta
        fields = ["nombre", "descripcion", "metodo"]
        labels = {
            "nombre": "Nombre de la receta",
            "descripcion": "Añade una descripcion",
            "metodo": "Preparacion"
        }

class RecetaIngredienteForm(forms.ModelForm):
    ingrediente_nombre = forms.CharField(label='Ingrediente', max_length=100)

    class Meta:
        model = RecetaIngrediente
        fields = ['ingrediente_nombre', 'cantidad']
    
RecetaIngredienteFormSet = forms.inlineformset_factory(
    Receta, RecetaIngrediente, form=RecetaIngredienteForm, extra=1, can_delete=True
)

class RestriccionesForm(forms.Form):
    restriccion = forms.CharField(
        max_length=100,
        label="Restricción alimentaria",
        widget=forms.TextInput(attrs={'placeholder': 'Ejemplo: Sin gluten'})
    )