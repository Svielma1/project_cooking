from django import forms
from .models import Ingrediente, Receta, RecetaIngrediente

class IngredienteForm(forms.ModelForm):
    class Meta:
        model = Ingrediente
        fields = ['nombre']


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