# categoria/serializers.py

# Importamos el módulo serializers de Django REST Framework
from rest_framework import serializers
# Importamos nuestro modelo Category
from .models import Category
# Importamos el modelo Product de la aplicación 'prenda'
from prenda.models import Product

# Serializador básico para el modelo Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        # Si tu modelo Product tiene 'created_at' y es de solo lectura, puedes añadirlo aquí:
        # read_only_fields = ('created_at',)

# Serializador principal para el modelo Category
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['id']

# Serializador para mostrar los detalles de una categoría junto con sus productos asociados
class CategoryDetailSerializer(serializers.ModelSerializer):
    # ¡LA LÍNEA CLAVE A MODIFICAR ES ESTA!
    # Eliminamos 'source='products'' porque el nombre del campo 'products'
    # ya coincide con el related_name del ForeignKey en el modelo Product.
    products = ProductSerializer(many=True, read_only=True) # <-- CAMBIO AQUÍ: Eliminado source='products'

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products']