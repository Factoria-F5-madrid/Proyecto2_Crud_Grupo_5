# categoria/views_api.py

# Importamos 'generics' de Django REST Framework, que nos da vistas preconstruidas para CRUD
from rest_framework import generics, status, filters
# Importamos Response para poder construir respuestas HTTP personalizadas.
from rest_framework.response import Response
# Importamos los errores de DRF para manejar excepciones específicas.
from rest_framework.exceptions import ValidationError, NotFound

# Importamos nuestro modelo Category.
from .models import Category
# Importamos ambos serializadores: el básico y el de detalle.
# Asegúrate de que CategoryDetailSerializer esté importado aquí.
from .serializers import CategorySerializer, CategoryDetailSerializer

# Vista para la colección de categorías (Listar y Crear)
# Permite:
#   - GET request a /api/categorias/ : Lista todas las categorías
#   - POST request a /api/categorias/ : Crea una nueva categoría
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all().prefetch_related('products')
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'id']
    ordering = ['name']

    # Sobreescribimos el método post para añadir manejo de errores personalizado
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            if 'name' in e.detail and 'already exists' in str(e.detail['name']):
                return Response({'detail': 'Category with this name already exists.'}, status=status.HTTP_409_CONFLICT)
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Vista para una categoría específica (Obtener, Actualizar, Eliminar)
# Permite:
#   - GET request a /api/categorias/<id>/ : Obtiene los detalles de una categoría específica (con productos anidados)
#   - PUT request a /api/categorias/<id>/ : Actualiza TODOS los campos de una categoría
#   - PATCH request a /api/categorias/<id>/ : Actualiza ALGUNOS campos de una categoría
#   - DELETE request a /api/categorias/<id>/ : Elimina una categoría
class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    lookup_field = 'pk'

    # ¡ESTE ES EL MÉTODO CLAVE QUE DEBEMOS ASEGURARNOS QUE ESTÉ CORRECTO!
    # Sobreescribimos get_serializer_class para usar el serializador de detalle en GET
    # y el serializador básico para PUT/PATCH.
    def get_serializer_class(self):
        # Si la petición es GET, usamos CategoryDetailSerializer para incluir los productos.
        if self.request.method == 'GET':
            return CategoryDetailSerializer
        # Para PUT, PATCH, DELETE (y por defecto), usamos el serializador básico.
        # Esto es porque no queremos que los clientes envíen datos de productos anidados
        # al actualizar o eliminar una categoría.
        return CategorySerializer

    # Sobreescribimos los métodos put, patch y delete para añadir manejo de errores personalizado
    # Aquí, llamamos explícitamente a CategorySerializer para las operaciones de escritura.
    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # Usamos el serializador básico para la actualización (PUT)
            serializer = CategorySerializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound:
            return Response({'detail': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            if 'name' in e.detail and 'already exists' in str(e.detail['name']):
                return Response({'detail': 'Category with this name already exists.'}, status=status.HTTP_409_CONFLICT)
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # Usamos el serializador básico para la actualización parcial (PATCH)
            serializer = CategorySerializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except NotFound:
            return Response({'detail': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as e:
            if 'name' in e.detail and 'already exists' in str(e.detail['name']):
                return Response({'detail': 'Category with this name already exists.'}, status=status.HTTP_409_CONFLICT)
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NotFound:
            return Response({'detail': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': 'An unexpected error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)