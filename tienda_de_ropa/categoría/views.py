from django.shortcuts import render, get_object_or_404, redirect
from .models import Category # Importa tu modelo Category
from .forms import CategoryForm # ¡Necesitarás crear este formulario!

#tienda_de_ropa/categoria/views.py

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categoria/category_list.html', {'categories': categories})

def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    # --- ¡NUEVA LÍNEA IMPORTANTE AQUÍ! ---
    # Accedemos a los productos relacionados usando el related_name='products'
    # que definiste en el ForeignKey del modelo Product en prenda/models.py
    productos_en_categoria = category.products.all() # Esto obtiene todos los productos relacionados

    context = {
        'category': category,
        'productos': productos_en_categoria, # Pasamos la lista de productos al template
    }
    return render(request, 'categoria/category_detail.html', context) # Pasamos el diccionario context

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('categoria:category_list')
    else:
        form = CategoryForm()
    return render(request, 'categoria/category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('categoria:category_detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categoria/category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('categoria:category_list')
    return render(request, 'categoria/category_confirm_delete.html', {'category': category})