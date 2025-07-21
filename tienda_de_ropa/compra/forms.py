from django import forms
from .models import Order, Customer # Importa Order y Customer (para el ForeignKey)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__' # Incluirá customer, order_date, total_amount, status

# Si decides hacer un formulario para OrderItem:
# class OrderItemForm(forms.ModelForm):
#     class Meta:
#         model = OrderItem
#         fields = '__all__' # Incluirá order, product, quantity, price