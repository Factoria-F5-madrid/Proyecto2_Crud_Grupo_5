from django.shortcuts import render, get_object_or_404, redirect
from .models import Product # Importa tu modelo Product
from .forms import ProductForm # ¡Necesitarás crear este formulario en el siguiente paso!

def product_list(request):
    products = Product.objects.all() # Obtiene todos los productos
    return render(request, 'prenda/product_list.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk) # Obtiene un producto por su PK o devuelve 404
    return render(request, 'prenda/product_detail.html', {'product': product})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST) # Crea un formulario con los datos enviados
        if form.is_valid(): # Valida los datos del formulario
            form.save() # Guarda el nuevo producto en la base de datos
            return redirect('prenda:product_list') # Redirige a la lista después de guardar
    else:
        form = ProductForm() # Crea un formulario vacío para GET (mostrar el formulario)
    return render(request, 'prenda/product_form.html', {'form': form})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk) # Obtiene el producto a actualizar
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product) # Rellena con datos enviados y la instancia existente
        if form.is_valid():
            form.save() # Guarda los cambios
            return redirect('prenda:product_detail', pk=product.pk) # Redirige al detalle
    else:
        form = ProductForm(instance=product) # Rellena con los datos actuales del producto para GET
    return render(request, 'prenda/product_form.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk) # Obtiene el producto a eliminar
    if request.method == 'POST':
        product.delete() # Elimina el producto
        return redirect('prenda:product_list') # Redirige a la lista
    # Para GET, simplemente muestra una página de confirmación
    return render(request, 'prenda/product_confirm_delete.html', {'product': product})