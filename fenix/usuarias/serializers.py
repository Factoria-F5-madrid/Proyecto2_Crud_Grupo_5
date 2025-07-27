from rest_framework import serializers
from .models import Usuaria
from django.core.validators import validate_email

class UsuariaSerializer(serializers.ModelSerializer):
    """
    Serializador completo para el modelo Usuaria con soporte para avatars.
    """
    # Campo para mostrar la URL completa del avatar
    avatar_url = serializers.SerializerMethodField()
    
    # Campo para mostrar el nombre completo (solo lectura)
    full_name = serializers.CharField(read_only=True)
    
    # Campo para mostrar el rol en español (solo lectura)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = Usuaria
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'phone', 'role', 'role_display', 'status', 'avatar', 'avatar_url',
            'hire_date', 'salary', 'address', 'is_active', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at', 'avatar_url', 'full_name', 'role_display')
        extra_kwargs = {
            'salary': {'write_only': True},  # El salario no se muestra en respuestas por seguridad
        }
    
    def get_avatar_url(self, obj):
        """Devuelve la URL completa del avatar"""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None
    
    def validate_email(self, value):
        """Validar formato de email"""
        validate_email(value)
        return value
    
    def validate_username(self, value):
        """Validar que el username no contenga espacios y sea alfanumérico"""
        if ' ' in value:
            raise serializers.ValidationError(
                "El nombre de usuario no puede contener espacios."
            )
        if not value.isalnum():
            raise serializers.ValidationError(
                "El nombre de usuario solo puede contener letras y números."
            )
        return value
    
    def validate_avatar(self, value):
        """Validar el archivo de avatar"""
        if value:
            # Validar tamaño del archivo (max 2MB)
            if value.size > 2 * 1024 * 1024:
                raise serializers.ValidationError(
                    "El archivo de avatar no puede ser mayor a 2MB."
                )
            
            # Validar tipo de archivo
            allowed_types = ['image/jpeg', 'image/png', 'image/webp', 'image/jpg']
            if value.content_type not in allowed_types:
                raise serializers.ValidationError(
                    "Solo se permiten archivos de imagen (JPEG, PNG, WEBP)."
                )
        
        return value

class UsuariaListSerializer(serializers.ModelSerializer):
    """
    Serializador simplificado para listado de usuarias (sin información sensible)
    """
    avatar_url = serializers.SerializerMethodField()
    full_name = serializers.CharField(read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = Usuaria
        fields = [
            'id', 'username', 'full_name', 'email', 'role', 'role_display',
            'status', 'avatar_url', 'is_active', 'created_at'
        ]
    
    def get_avatar_url(self, obj):
        """Devuelve la URL completa del avatar"""
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return None

class UsuariaCreateSerializer(serializers.ModelSerializer):
    """
    Serializador específico para crear usuarias con validaciones especiales
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        required=False,
        help_text="Contraseña mínima de 8 caracteres (opcional)"
    )
    password_confirm = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = Usuaria
        fields = [
            'username', 'email', 'first_name', 'last_name', 'phone',
            'role', 'status', 'avatar', 'hire_date', 'salary', 'address',
            'password', 'password_confirm'
        ]
        extra_kwargs = {
            'salary': {'required': False},
        }
    
    def validate(self, attrs):
        """Validar que las contraseñas coincidan si se proporcionan"""
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm', None)
        
        # Solo validar contraseñas si se proporcionan
        if password or password_confirm:
            if password != password_confirm:
                raise serializers.ValidationError(
                    "Las contraseñas no coinciden."
                )
        
        return attrs
    
    def create(self, validated_data):
        """Crear usuaria con contraseña hasheada"""
        # Extraer la contraseña para procesarla por separado
        password = validated_data.pop('password', None)
        
        # Crear la usuaria
        usuaria = Usuaria.objects.create(**validated_data)
        
        # Si se proporcionó contraseña, se podría usar para autenticación futura
        # (Este modelo no extiende User, así que solo guardamos la usuaria)
        
        return usuaria
