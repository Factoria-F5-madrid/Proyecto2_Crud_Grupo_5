from rest_framework import serializers
from .models import Product
from categoría.serializers import CategorySerializer

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Product con soporte para imágenes.
    Convierte instancias de Product a JSON y viceversa.
    """
    # Campo para mostrar la URL completa de la imagen
    image_url = serializers.SerializerMethodField()
    
    # Campo para mostrar información de la categoría (solo lectura)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'size', 'color', 'price', 'stock', 'description',
            'image', 'image_url', 'category', 'category_name', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at', 'image_url', 'category_name')
    
    def get_image_url(self, obj):
        """Devuelve la URL completa de la imagen"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def validate_image(self, value):
        """Validar el archivo de imagen"""
        if value:
            # Validar tamaño del archivo (max 5MB)
            if value.size > 5 * 1024 * 1024:
                raise serializers.ValidationError(
                    "El archivo de imagen no puede ser mayor a 5MB."
                )
            
            # Validar tipo de archivo
            allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/jpg']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    "Solo se permiten archivos de imagen (JPEG, PNG, WEBP)."
                )
        
        return value

class ProductListSerializer(serializers.ModelSerializer):
    """
    Serializador simplificado para listado de productos (sin imagen completa)
    """
    image_url = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'size', 'color', 'price', 'stock',
            'image_url', 'category', 'category_name', 'created_at'
        ]
    
    def get_image_url(self, obj):
        """Devuelve la URL completa de la imagen"""
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
