# prenda/urls_api.py
from django.urls import path
from .api_views import ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView # Tus vistas REST
# Si tienes vistas basadas en funciones para HTML en views.py,
# las importarías así: from . import views

app_name = 'prenda_api' # Un nuevo namespace para las URLs de API de 'prenda'

urlpatterns = [
    # URLs para la API REST de productos.
    # No tienen prefijo 'api/' aquí, se añadirá en el urls.py principal.
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
]