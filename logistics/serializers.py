from rest_framework import serializers
from .models import Shipment
from core.models import Category
from clients.serializers import ClientListSerializer # Asumiendo que tienes un serializador simple en tu app de clientes

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Category.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ShipmentSerializer(serializers.ModelSerializer):
    """
    Serializador para crear y actualizar Shipments.
    Maneja IDs para las relaciones.
    """
    class Meta:
        model = Shipment
        fields = '__all__'

class ShipmentListSerializer(serializers.ModelSerializer):
    """
    Serializador optimizado para listar Shipments.
    Muestra información detallada de los modelos relacionados (nested).
    """
    # Usamos serializadores anidados para mostrar los datos del cliente y la categoría
    client = ClientListSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Shipment
        # Seleccionamos los campos más relevantes para la vista de lista
        fields = [
            'id', 
            'shipment_code', 
            'client', 
            'category', 
            'recipient_name', 
            'price', 
            'is_invoiced', 
            'created_at'
        ]