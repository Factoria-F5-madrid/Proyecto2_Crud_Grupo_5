import django_filters
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from .models import Prenda
from .froms import PrendaForm
from .serializers import PrendaSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, get_object_or_404, redirect

class PrendaFilter(django_filters.FilterSet):
    min_stock = django_filters.NumberFilter(field_name="stock", lookup_expr='gte')
    max_stock = django_filters.NumberFilter(field_name="stock", lookup_expr="lte")
    min_precio = django_filters.NumberFilter(field_name="precio", lookup_expr='gte')
    max_precio = django_filters.NumberFilter(field_name="precio", lookup_expr='lte')
    
    class Meta:
        model = Prenda
        fields = ['categoria']

class PrendaViewSet(viewsets.ModelViewSet):
    queryset = Prenda.objects.all()
    serializer_class = PrendaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['nombre', 'descripcion']
    filterset_class = PrendaFilter
    
def prenda_list(requests):
    prenda = Prenda.objects.all()
    return render(requests, 'prende/prenda_list.html', {'prenda': prenda})

def prenda_detail(request, pk):
    prenda = get_object_or_404(Prenda, pk=pk)
    return render(request, 'prenda/prenda_detail.html', {'prenda': prenda})

def prenda_create(request):
    if request.method == 'POST':
        form = PrendaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('prenda:prenda_list')
        else:
            form = PrendaForm()
        return render(request, 'prenda/prenda_form.html', {'form': form})
    
def prenda_update(request, pk):
    prenda = get_object_or_404(Prenda, pk=pk)
    if request.method == 'POST':
        prenda.delete()
        return redirect('prenda:prenda_list')
    return render(request, 'prenda/prenda_confirm_delete.html', {'prenda': prenda})