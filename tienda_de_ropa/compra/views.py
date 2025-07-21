# C:\Users\Coder\OneDrive - uniminuto.edu\Curso Programación\bootcamp_ia\RopaCrud\Proyecto2_Crud_Grupo_5\tienda_de_ropa\compra\views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem
from .forms import OrderForm
import logging 

logger = logging.getLogger('compra') 

def order_list(request):
    logger.info("Accediendo a la lista de pedidos.") # Añadido para el logging
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'compra/order_list.html', {'orders': orders})

def order_detail(request, pk):
    logger.debug(f"Accediendo al detalle del pedido con ID: {pk}") # Añadido para el logging
    order = get_object_or_404(Order, pk=pk)
    # Cambia esta línea:
    order_items = order.items.all() # <--- ¡AQUÍ ESTÁ EL CAMBIO!
    return render(request, 'compra/order_detail.html', {'order': order, 'order_items': order_items})

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save() # Captura la instancia del pedido creado
            logger.info(f"Pedido creado exitosamente con ID: {order.pk}") # Añadido para el logging
            return redirect('compra:order_list')
        else:
            logger.warning(f"Intento fallido de creación de pedido. Errores: {form.errors}") # Añadido para el logging
    else:
        form = OrderForm()
    return render(request, 'compra/order_form.html', {'form': form})

def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            logger.info(f"Pedido con ID {pk} actualizado exitosamente.") # Añadido para el logging
            return redirect('compra:order_detail', pk=order.pk)
        else:
            logger.error(f"Error al actualizar el pedido con ID {pk}. Errores: {form.errors}") # Añadido para el logging
    else:
        form = OrderForm(instance=order)
    return render(request, 'compra/order_form.html', {'form': form})

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        logger.critical(f"Pedido con ID {pk} eliminado permanentemente.") # Añadido para el logging
        return redirect('compra:order_list')
    return render(request, 'compra/order_confirm_delete.html', {'order': order})

# Si decides hacer CRUD para OrderItem, sus vistas irían aquí:
# def order_item_list(request):
#     items = OrderItem.objects.all()
#     return render(request, 'compra/order_item_list.html', {'items': items})
# ...