from django import forms
from .models import Prenda # Importa tu modelo Product

class PrendaForm(forms.ModelForm):
    class Meta:
        model = Prenda
        fields = '__all__' # Incluye todos los campos del modelo en el formulario
        # Si quieres ser más específico, puedes listar los campos:
        # fields = ['name', 'size', 'color', 'price', 'stock', 'category']