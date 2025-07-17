from rest_framework import serializers# <--- ¡Esta es la línea CORRECTA!
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
import re # Importamos para validaciones de complejidad de contraseña

# Obtener el modelo de usuario activo en Django (generalmente django.contrib.auth.models.User)
User = get_user_model()

# Serializer básico para representar un usuario
# Se usa para mostrar datos de usuario, no para crear/actualizar con validaciones complejas.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Ajusta los campos según lo que quieras exponer del usuario
        fields = ('id', 'username', 'email')

# Serializer para el registro de nuevos usuarios
# Contiene todas las validaciones necesarias para la creación de una cuenta.
class RegisterSerializer(serializers.ModelSerializer):
    # Campo para la contraseña: solo escritura, obligatorio, con estilo de input tipo password.
    # Se añade validación de longitud mínima.
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8, # Validación: La contraseña debe tener al menos 8 caracteres
        error_messages={
            'required': 'La contraseña es obligatoria.',
            'min_length': 'La contraseña debe tener al menos 8 caracteres.'
        }
    )
    # Campo para la confirmación de la contraseña: solo escritura, obligatorio.
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        error_messages={
            'required': 'La confirmación de la contraseña es obligatoria.'
        }
    )

    class Meta:
        model = User
        # Campos que se esperan en la petición de registro
        fields = ('username', 'password', 'password2', 'email')
        # Configuraciones extra para campos, como marcarlos como solo escritura.
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {
                'required': True,
                'allow_blank': False,
                'error_messages': {
                    'required': 'El nombre de usuario es obligatorio.',
                    'blank': 'El nombre de usuario no puede estar en blanco.'
                }
            },
            'email': {
                'required': True, # Hacemos el email obligatorio para el registro
                'allow_blank': False,
                'error_messages': {
                    'required': 'El correo electrónico es obligatorio.',
                    'blank': 'El correo electrónico no puede estar en blanco.'
                }
            }
        }

    # Validación a nivel de campo para 'username'
    # Se utiliza UniqueValidator para personalizar el mensaje de error de unicidad.
    username = serializers.CharField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Este nombre de usuario ya está en uso. Por favor, elige otro."
            )
        ],
        required=True,
        allow_blank=False,
        min_length=3, # Ejemplo: nombre de usuario mínimo 3 caracteres
        error_messages={
            'required': 'El nombre de usuario es obligatorio.',
            'blank': 'El nombre de usuario no puede estar en blanco.',
            'min_length': 'El nombre de usuario debe tener al menos 3 caracteres.'
        }
    )

    # Validación a nivel de campo para 'email'
    # Se utiliza UniqueValidator para personalizar el mensaje de error de unicidad.
    email = serializers.EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Este correo electrónico ya está registrado. Por favor, inicia sesión o usa otro."
            )
        ],
        required=True,
        allow_blank=False,
        error_messages={
            'required': 'El correo electrónico es obligatorio.',
            'blank': 'El correo electrónico no puede estar en blanco.',
            'invalid': 'Por favor, introduce un formato de correo electrónico válido.'
        }
    )

    # Método de validación a nivel de objeto.
    # Se ejecuta después de las validaciones de campo individuales.
    def validate(self, attrs):
        # 1. Validación de coincidencia de contraseñas.
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password2": "Las contraseñas no coinciden."})

        # 2. Validación de complejidad de contraseña: al menos un número, una mayúscula y una minúscula.
        password = attrs['password']
        if not re.search(r'\d', password): # Verifica si hay al menos un dígito
            raise serializers.ValidationError({"password": "La contraseña debe contener al menos un número."})
        if not re.search(r'[A-Z]', password): # Verifica si hay al menos una letra mayúscula
            raise serializers.ValidationError({"password": "La contraseña debe contener al menos una letra mayúscula."})
        if not re.search(r'[a-z]', password): # Verifica si hay al menos una letra minúscula
            raise serializers.ValidationError({"password": "La contraseña debe contener al menos una letra minúscula."})

        # Siempre devuelve los atributos validados.
        return attrs

    # Método para crear un nuevo usuario.
    def create(self, validated_data):
        # Elimina 'password2' ya que no es un campo del modelo User.
        validated_data.pop('password2')
        # Crea el usuario usando el método create_user del manager del modelo User.
        user = User.objects.create_user(**validated_data)
        return user

# Serializer para cambiar la contraseña
# Es un Serializer normal porque no mapea directamente a un modelo para creación/actualización general.
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        error_messages={'required': 'La contraseña actual es obligatoria.'}
    )
    new_password = serializers.CharField(
        required=True,
        style={'input_type': 'password'},
        min_length=8, # Nueva contraseña debe tener al menos 8 caracteres
        error_messages={
            'required': 'La nueva contraseña es obligatoria.',
            'min_length': 'La nueva contraseña debe tener al menos 8 caracteres.'
        }
    )

    # Método de validación a nivel de objeto para ChangePasswordSerializer.
    def validate(self, data):
        # 1. Validación de complejidad de la nueva contraseña.
        new_password = data.get('new_password')
        if not re.search(r'\d', new_password):
            raise serializers.ValidationError({"new_password": "La nueva contraseña debe contener al menos un número."})
        if not re.search(r'[A-Z]', new_password):
            raise serializers.ValidationError({"new_password": "La nueva contraseña debe contener al menos una letra mayúscula."})
        if not re.search(r'[a-z]', new_password):
            raise serializers.ValidationError({"new_password": "La nueva contraseña debe contener al menos una letra minúscula."})

        # 2. Validación de que la nueva contraseña no sea igual a la antigua.
        if data.get('old_password') == data.get('new_password'):
            raise serializers.ValidationError({"new_password": "La nueva contraseña no puede ser igual a la anterior."})

        # Siempre devuelve los atributos validados.
        return data
        