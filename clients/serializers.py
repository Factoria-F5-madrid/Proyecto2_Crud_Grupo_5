from rest_framework import serializers
from .models import Client

class ClientSerializer(serializers.ModelSerializer):
    """
    Serializador completo para el detalle, creación y edición.
    """
    class Meta:
        model = Client
        fields = [
            'id', 
            'client_code', 
            'legal_name', 
            'tax_id', 
            'address', 
            'location', 
            'email', 
            'phone', 
            'vat_rate', 
            'payment_term', 
            'is_active', 
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class ClientListSerializer(serializers.ModelSerializer):
    """
    Serializador simple solo para mostrar en listas anidadas de otros modelos.
    """
    class Meta:
        model = Client
        fields = ['id', 'legal_name']