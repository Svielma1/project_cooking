from django import forms
from .models import Ingrediente, Receta, RecetaIngrediente
from django.contrib.auth.models import User

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")
    username = forms.CharField(
        max_length=50, 
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'placeholder': 'Ingresa tu nombre de usuario'}),
        help_text=""  # Quita el mensaje predeterminado
    )

    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")

    class Meta:
        model = User
        fields = ['username']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
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