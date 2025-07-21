from django.shortcuts import render, get_object_or_404, redirect
from .models import Customer # Importa tu modelo Customer
from .forms import CustomerForm # ¡Necesitarás crear este formulario!

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'cliente/customer_list.html', {'customers': customers})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'cliente/customer_detail.html', {'customer': customer})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cliente:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'cliente/customer_form.html', {'form': form})

def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('cliente:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'cliente/customer_form.html', {'form': form})

def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('cliente:customer_list')
    return render(request, 'cliente/customer_confirm_delete.html', {'customer': customer})