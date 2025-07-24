from django.shortcuts import render, get_object_or_404, redirect
from .models import Category # Importa tu modelo Category
from .forms import CategoryForm # ¡Necesitarás crear este formulario!
import logging
logger = logging.getLogger('categoria')

#tienda_de_ropa/categoria/views.py

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'categoria/category_list.html', {'categories': categories})

def category_detail(request, pk):

   logger.info(f"Accediendo al detalle de la categoría con ID: {pk}")
   category = get_object_or_404(Category, pk=pk)
   products_in_category = category.products.all()
   
   return render(request, 'categoria/category_detail.html', {
        'category': category,
        'products': products_in_category # <--- Añadido
    })
    
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