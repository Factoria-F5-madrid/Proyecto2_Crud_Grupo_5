
from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem
from .forms import OrderForm
import logging
from django.contrib import messages # <--- ¡Añade esta importación para los mensajes!

logger = logging.getLogger('compra')

def order_list(request):
    logger.info("Accediendo a la lista de pedidos.")
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'compra/order_list.html', {'orders': orders})

def order_detail(request, pk):
    logger.debug(f"Accediendo al detalle del pedido con ID: {pk}")
    order = get_object_or_404(Order, pk=pk)
    order_items = order.items.all()
    return render(request, 'compra/order_detail.html', {'order': order, 'order_items': order_items})

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            try:
                order = form.save() # Captura la instancia del pedido creado
                logger.info(f"Pedido creado exitosamente con ID: {order.pk}")
                messages.success(request, f"Pedido #{order.pk} creado exitosamente.") # Mensaje de éxito
                return redirect('compra:order_list')
            except Exception as e:
                # Captura cualquier excepción inesperada durante el guardado
                logger.error(f"Error inesperado al crear pedido: {e}", exc_info=True) # exc_info=True para el traceback
                messages.error(request, f"Ocurrió un error al intentar crear el pedido. Por favor, inténtelo de nuevo.") # Mensaje de error para el usuario
        else:
            # El formulario no es válido, los errores ya están en form.errors
            logger.warning(f"Intento fallido de creación de pedido. Errores: {form.errors}")
            messages.error(request, f"Por favor, corrija los errores en el formulario para crear el pedido.") # Mensaje para errores de validación
    else:
        form = OrderForm()
    return render(request, 'compra/order_form.html', {'form': form})

def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            try:
                form.save()
                logger.info(f"Pedido con ID {pk} actualizado exitosamente.")
                messages.success(request, f"Pedido #{pk} actualizado exitosamente.") # Mensaje de éxito
                return redirect('compra:order_detail', pk=order.pk)
            except Exception as e:
                # Captura cualquier excepción inesperada durante la actualización
                logger.error(f"Error inesperado al actualizar el pedido con ID {pk}: {e}", exc_info=True)
                messages.error(request, f"Ocurrió un error al intentar actualizar el pedido #{pk}. Por favor, inténtelo de nuevo.") # Mensaje de error para el usuario
        else:
            logger.error(f"Error al actualizar el pedido con ID {pk}. Errores: {form.errors}")
            messages.error(request, f"Por favor, corrija los errores en el formulario para actualizar el pedido.") # Mensaje para errores de validación
    else:
        form = OrderForm(instance=order)
    return render(request, 'compra/order_form.html', {'form': form})

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        try:
            order.delete()
            logger.critical(f"Pedido con ID {pk} eliminado permanentemente.")
            messages.success(request, f"Pedido #{pk} eliminado exitosamente.") # Mensaje de éxito
            return redirect('compra:order_list')
        except Exception as e:
            # Captura cualquier excepción inesperada durante la eliminación
            logger.error(f"Error inesperado al eliminar el pedido con ID {pk}: {e}", exc_info=True)
            messages.error(request, f"Ocurrió un error al intentar eliminar el pedido #{pk}. No se pudo eliminar.") # Mensaje de error
    return render(request, 'compra/order_confirm_delete.html', {'order': order})

# ... (Si decidimos hacer hacer CRUD para OrderItem (si el tiempo nos da), las vistas irían aquí) ...