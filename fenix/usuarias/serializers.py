from rest_framework import serializers
from .models import Usuaria

class DatosUsuariaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuaria
        fields = ['id', 'nombre', 'email', 'telefono', 'direccion']  # Incluye aquí todos los campos que tengas en tu modelo
