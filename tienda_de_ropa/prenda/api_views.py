# prenda/views.py
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
# Asegúrate de que no haya conflicto si ya tienes vistas basadas en funciones aquí.
# Si ya tienes views.py para HTML, crea un archivo nuevo como prenda/api_views.py
# y ajusta los imports en urls.py en consecuencia.
# Por simplicidad, asumiré que puedes añadir estas aquí.

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