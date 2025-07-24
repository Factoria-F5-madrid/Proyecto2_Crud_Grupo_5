# prenda/views.py
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view # Importamos este decorador
from rest_framework.response import Response # Para devolver respuestas de DRF
from django.http import HttpResponse # Necesario para HttpResponse
import csv # Necesario para manejar archivos CSV
# Asegúrate de que no haya conflicto si ya tienes vistas basadas en funciones aquí.
# Si ya tienes views.py para HTML, crea un archivo nuevo como prenda/api_views.py
# y ajusta los imports en urls.py en consecuencia.

class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    Vista para listar todos los productos o crear uno nuevo.
    - GET /products/ (Lista todos los productos)
    - POST /products/ (Crea un nuevo producto)
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para recuperar, actualizar o eliminar un producto específico.
    - GET /products/{id}/ (Obtiene los detalles de un producto)
    - PUT /products/{id}/ (Actualiza un producto existente)
    - PATCH /products/{id}/ (Actualiza parcialmente un producto existente)
    - DELETE /products/{id}/ (Elimina un producto)
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk' # Usa 'pk' (clave primaria) para buscar el objeto

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

