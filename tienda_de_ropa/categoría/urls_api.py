# tienda_de_ropa/categoría/urls_api.py

# Importamos la función path para definir rutas URL
from django.urls import path
# Importamos nuestras vistas API que acabamos de crear (ahora desde views_api)
from .views_api import CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView # Cambiado a .views_api

# 'app_name' es un identificador único para este conjunto de URLs.
# Ayuda a evitar confusiones si otras apps tienen URLs con los mismos nombres.
app_name = 'categoría_api'

# 'urlpatterns' es la lista donde definimos todas nuestras rutas de la API
urlpatterns = [
    # Ruta para la lista de categorías y para crear una nueva categoría.
    # Cuando se acceda a '/api/categorias/' (porque la incluiremos con un prefijo),
    # esta ruta manejará los GET (listar) y POST (crear).
    # 'name' es un nombre interno para referenciar esta URL en nuestro código.
    path('', CategoryListCreateAPIView.as_view(), name='category-list-create'),

    # Ruta para una categoría específica (obtener, actualizar, eliminar).
    # Cuando se acceda a '/api/categorias/<un_numero>/', por ejemplo /api/categorias/1/,
    # esta ruta manejará los GET (detalle), PUT/PATCH (actualizar) y DELETE (eliminar).
    # '<int:pk>' significa que esperamos un número entero (int) que llamaremos 'pk' (Primary Key/ID).
    # Puedes omitirlo si usas 'pk', pero lo pongo para que sepan qué significa.
    path('<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
]
