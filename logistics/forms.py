from django import forms
from .models import Shipment

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ['name', 'description', 'price']
        
        # Opcional: añade widgets para mejorar la apariencia en las plantillas
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_price(self):
        """
        Añade validación personalizada para asegurar que el precio no sea negativo.
        """
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("El precio no puede ser negativo.")
        return price