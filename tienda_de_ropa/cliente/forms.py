from django import forms
from .models import Customer # Importa tu modelo Customer

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'