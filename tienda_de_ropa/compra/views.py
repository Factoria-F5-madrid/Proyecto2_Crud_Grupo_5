# compra/views.py
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy # Necesario para redirecciones en Class-Based Views
from django.contrib import messages # Para mensajes flash, si los usas
from django.db import transaction # Para asegurar atomicidad en operaciones complejas

from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm # Asegúrate de que OrderItemForm exista en forms.py

logger = logging.getLogger(__name__)

# Vistas para el modelo Order (Pedido)
class OrderListView(ListView):
    model = Order
    template_name = 'compra/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10 # Opcional: paginar los resultados

    def get_queryset(self):
        logger.info("Accediendo a la lista de pedidos.")
        return Order.objects.all().order_by('-order_date') # Asegura ordenación


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'compra/order_form.html'
    # success_url se obtendrá del get_absolute_url del modelo Order tras la creación

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"Pedido creado exitosamente con ID: {self.object.pk}")
        messages.success(self.request, f"Pedido #{self.object.pk} creado exitosamente.")
        return response

    def form_invalid(self, form):
        logger.warning(f"Intento fallido de creación de pedido. Errores: {form.errors.as_ul()}")
        messages.error(self.request, "Por favor, corrija los errores en el formulario.")
        return super().form_invalid(form)


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'compra/order_form.html'
    # ***** CAMBIO AQUÍ: Sin success_url explícito, usará get_absolute_url del modelo *****
    # success_url = reverse_lazy('compra:order_list') # Comentada o eliminada

    def form_valid(self, form):
        response = super().form_valid(form)
        logger.info(f"Pedido con ID {self.object.pk} actualizado exitosamente.")
        messages.success(self.request, f"Pedido #{self.object.pk} actualizado exitosamente.")
        return response

    def form_invalid(self, form):
        logger.error(f"Error al actualizar el pedido con ID {self.object.pk}. Errores: {form.errors.as_ul()}")
        messages.error(self.request, "Hubo un error al actualizar el pedido. Por favor, revise.")
        return super().form_invalid(form)


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'compra/order_confirm_delete.html'
    success_url = reverse_lazy('compra:order_list')

    def form_valid(self, form):
        order_id = self.object.pk
        response = super().form_valid(form)
        logger.critical(f"Pedido con ID {order_id} eliminado permanentemente.")
        messages.success(self.request, f"Pedido #{order_id} eliminado exitosamente.")
        return response


# Vista basada en función para el detalle de Order (porque maneja OrderItems)
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    # Accede a los ítems del pedido a través del related_name 'items'
    order_items = order.items.all()
    context = {
        'order': order,
        'order_items': order_items
    }
    return render(request, 'compra/order_detail.html', context)


# Vistas para el modelo OrderItem (Ítem de Pedido) - Si los vas a implementar
# Class-Based Views para OrderItem:

# class OrderItemCreateView(CreateView):
#     model = OrderItem
#     form_class = OrderItemForm
#     template_name = 'compra/orderitem_form.html'
#     # Puedes redirigir al detalle del pedido al que pertenece el OrderItem
#     def get_success_url(self):
#         return reverse_lazy('compra:order_detail', kwargs={'pk': self.object.order.pk})

# class OrderItemUpdateView(UpdateView):
#     model = OrderItem
#     form_class = OrderItemForm
#     template_name = 'compra/orderitem_form.html'
#     # Puedes redirigir al detalle del pedido al que pertenece el OrderItem
#     def get_success_url(self):
#         return reverse_lazy('compra:order_detail', kwargs={'pk': self.object.order.pk})

# class OrderItemDeleteView(DeleteView):
#     model = OrderItem
#     template_name = 'compra/orderitem_confirm_delete.html'
#     # Puedes redirigir al detalle del pedido al que pertenecía el OrderItem
#     def get_success_url(self):
#         return reverse_lazy('compra:order_detail', kwargs={'pk': self.object.order.pk})