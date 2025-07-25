from django.urls import path
from .api_views import (
    ProductListCreateAPIView,
    ProductRetrieveUpdateDestroyAPIView,
    export_products_csv_api,
)

app_name = 'prenda_api'  # Namespace para la API de prendas

urlpatterns = [
    # Ruta para exportar productos en CSV (antes que <int:pk> para evitar conflictos)
    path('products/export-csv/', export_products_csv_api, name='product-export-csv'),
    
    # Listar productos y crear uno nuevo
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    
    # Obtener, actualizar o eliminar producto por id
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
]
