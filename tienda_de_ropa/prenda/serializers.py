from rest_framework import serializers
from .models import Prenda

class PrendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prenda
        fields = '__all__'