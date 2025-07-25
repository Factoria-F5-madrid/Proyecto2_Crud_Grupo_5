from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
import csv
from .models import Product
from .serializers import ProductSerializer, ProductListSerializer
from django_filters import rest_framework as django_filters

class ProductFilter(django_filters.FilterSet):
    """Custom filter for products"""
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    stock_min = django_filters.NumberFilter(field_name="stock", lookup_expr='gte')
    
    class Meta:
        model = Product
        fields = {
            'category': ['exact'],
            'size': ['exact', 'icontains'],
            'color': ['exact', 'icontains'],
        }

class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    Vista para listar todos los productos o crear uno nuevo.
    - GET /api/products/ (Lista todos los productos con filtros)
    - POST /api/products/ (Crea un nuevo producto con imagen)
    
    Filtros disponibles:
    - ?search=nombre (busca en nombre)
    - ?category=1 (filtra por categoría)
    - ?size=M (filtra por talla)
    - ?color=azul (filtra por color)
    - ?price_min=10&price_max=100 (rango de precios)
    - ?stock_min=5 (stock mínimo)
    - ?ordering=price,-created_at (ordena por campos)
    
    Para subir imagen: usar Content-Type: multipart/form-data
    """
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'price', 'stock', 'created_at']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        """Use different serializers for list vs detail"""
        if self.request.method == 'GET':
            return ProductListSerializer
        return ProductSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para recuperar, actualizar o eliminar un producto específico.
    - GET /api/products/{id}/ (Obtiene los detalles de un producto)
    - PUT /api/products/{id}/ (Actualiza un producto existente con imagen)
    - PATCH /api/products/{id}/ (Actualiza parcialmente un producto existente)
    - DELETE /api/products/{id}/ (Elimina un producto)
    
    Para actualizar imagen: usar Content-Type: multipart/form-data
    """
    queryset = Product.objects.all().select_related('category')
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser, JSONParser]
    lookup_field = 'pk'
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- NUEVA VISTA DE API para exportar productos a CSV ---
@api_view(['GET']) # Indica que esta vista solo acepta solicitudes GET
def export_products_csv_api(request):
    """
    Vista de API para exportar todos los productos a un archivo CSV.
    Accesible via GET a /api/products/export-csv/
    """
    # 1. Crear la respuesta HTTP con el tipo de contenido CSV
    response = HttpResponse(content_type='text/csv')
    
    # 2. Establecer el encabezado 'Content-Disposition' para forzar la descarga
    response['Content-Disposition'] = 'attachment; filename="productos.csv"'

    # 3. Crear un escritor CSV que escribirá directamente en la respuesta HTTP
    writer = csv.writer(response)

    # 4. Escribir la fila de encabezados (nombres de las columnas)
    writer.writerow(['ID', 'Nombre', 'Talla', 'Color', 'Precio', 'Stock', 'ID Categoria', 'Fecha Creacion'])

    # 5. Obtener los datos de los productos y escribirlos en el CSV
    products = Product.objects.all().order_by('id')

    for product in products:
        category_id = product.category.id if product.category else ''
        writer.writerow([
            product.id,
            product.name,
            product.size,
            product.color,
            product.price,
            product.stock,
            category_id,
            product.created_at.strftime('%Y-%m-%d %H:%M:%S') # Formatear la fecha
        ])

    return response

