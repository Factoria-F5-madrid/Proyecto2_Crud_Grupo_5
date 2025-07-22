# prenda/serializers.py
from rest_framework import serializers
from .models import Product # Importa el modelo Product

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Product.
    Convierte instancias de Product a JSON y viceversa.
    """
    class Meta:
        model = Product
        fields = '__all__' # Incluye todos los campos del modelo
        # O si prefieres especificar:
        # fields = ['id', 'name', 'size', 'color', 'price', 'stock', 'category', 'created_at']
        read_only_fields = ('created_at',) # Campos que no se pueden modificar en la creación/actualización