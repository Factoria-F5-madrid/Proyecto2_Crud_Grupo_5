from rest_framework import serializers
from .models import Customer # Importa el modelo Customer

class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Customer.
    Convierte instancias de Customer a JSON y viceversa.
    """
    class Meta:
        model = Customer
        fields = '__all__' # Incluye todos los campos del modelo
        read_only_fields = ('created_at',) # 'created_at' no se debe modificar en la creación/actualización