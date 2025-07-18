from django import forms
from .models import Product # Importa tu modelo Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__' # Incluye todos los campos del modelo en el formulario
        # Si quieres ser más específico, puedes listar los campos:
        # fields = ['name', 'size', 'color', 'price', 'stock', 'category']