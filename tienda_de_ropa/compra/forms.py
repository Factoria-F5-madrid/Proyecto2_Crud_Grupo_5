from django import forms
from .models import Order, Customer, OrderItem # Importa Order y Customer (para el ForeignKey)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'
        # widgets = {
        #     'order_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        # }


class OrderItemForm(forms.ModelForm): # <--- Asegúrate de que esta clase exista
    class Meta:
        model = OrderItem
        fields = '__all__'