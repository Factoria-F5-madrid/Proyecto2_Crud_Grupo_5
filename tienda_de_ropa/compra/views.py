from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem # Importa ambos modelos
from .forms import OrderForm # ¡Necesitarás crear este formulario!

def order_list(request):
    orders = Order.objects.all().order_by('-order_date') # Ordena por fecha descendente
    return render(request, 'compra/order_list.html', {'orders': orders})

def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    # Puedes obtener los items asociados al pedido para mostrarlos en el detalle
    order_items = order.orderitem_set.all()
    return render(request, 'compra/order_detail.html', {'order': order, 'order_items': order_items})

def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('compra:order_list')
    else:
        form = OrderForm()
    return render(request, 'compra/order_form.html', {'form': form})

def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('compra:order_detail', pk=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'compra/order_form.html', {'form': form})

def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('compra:order_list')
    return render(request, 'compra/order_confirm_delete.html', {'order': order})

# Si decides hacer CRUD para OrderItem, sus vistas irían aquí:
# def order_item_list(request):
#     items = OrderItem.objects.all()
#     return render(request, 'compra/order_item_list.html', {'items': items})
# ...