from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import ServiceCategory, Service # Importa tus modelos ServiceCategory y Service

# Serializer para el modelo ServiceCategory
class ServiceCategorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        required=True,
        allow_blank=False, # El nombre no puede estar en blanco
        validators=[
            UniqueValidator(
                queryset=ServiceCategory.objects.all(),
                message="Ya existe una categoría de servicio con este nombre. Debe ser único."
            )
        ],
        error_messages={
            'required': 'El nombre de la categoría es obligatorio.',
            'blank': 'El nombre de la categoría no puede estar en blanco.',
            'max_length': 'El nombre de la categoría no puede exceder los 100 caracteres.'
        }
    )

    description = serializers.CharField(
        required=False, # Es opcional (blank=True en el modelo)
        allow_blank=True, # Puede estar en blanco
        style={'base_template': 'textarea.html'}
    )

    is_active = serializers.BooleanField(
        required=False, # Es opcional, tiene un default en el modelo
        error_messages={
            'invalid': 'El valor para "activo" debe ser verdadero o falso.'
        }
    )

    class Meta:
        model = ServiceCategory
        fields = '__all__' # Incluye todos los campos del modelo ServiceCategory
        # read_only_fields para campos auto-gestionados
        read_only_fields = ('created_at', 'updated_at')

    # No hay validaciones cruzadas complejas en ServiceCategory por ahora,
    # por lo que no necesitamos un método validate() a nivel de objeto.


# Serializer para el modelo Service
class ServiceSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=200,
        required=True,
        allow_blank=False, # El nombre no puede estar en blanco
        error_messages={
            'required': 'El nombre del servicio es obligatorio.',
            'blank': 'El nombre del servicio no puede estar en blanco.',
            'max_length': 'El nombre del servicio no puede exceder los 200 caracteres.'
        }
    )

    code = serializers.CharField(
        max_length=20,
        required=True,
        allow_blank=False, # El código no puede estar en blanco
        validators=[
            UniqueValidator(
                queryset=Service.objects.all(),
                message="Ya existe un servicio con este código. Debe ser único."
            )
        ],
        error_messages={
            'required': 'El código del servicio es obligatorio.',
            'blank': 'El código del servicio no puede estar en blanco.',
            'max_length': 'El código del servicio no puede exceder los 20 caracteres.'
        }
    )

    description = serializers.CharField(
        required=False, # Es opcional (blank=True en el modelo)
        allow_blank=True, # Puede estar en blanco
        style={'base_template': 'textarea.html'}
    )

    category = serializers.PrimaryKeyRelatedField(
        queryset=ServiceCategory.objects.all(), # Asegura que el ID de la categoría exista
        error_messages={
            'does_not_exist': 'La categoría de servicio con el ID proporcionado no existe.',
            'required': 'La categoría del servicio es obligatoria.'
        }
    )

    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01, # El precio debe ser un valor positivo
        required=True,
        error_messages={
            'required': 'El precio del servicio es obligatorio.',
            'min_value': 'El precio del servicio debe ser mayor que cero.',
            'invalid': 'Por favor, introduce un valor numérico válido para el precio.'
        }
    )

    tax_percentage = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0.00, # El porcentaje de IVA puede ser 0
        max_value=100.00, # El porcentaje de IVA no puede exceder 100
        required=False, # Es opcional (tiene un default en el modelo)
        error_messages={
            'min_value': 'El porcentaje de IVA no puede ser negativo.',
            'max_value': 'El porcentaje de IVA no puede exceder 100.',
            'invalid': 'Por favor, introduce un valor numérico válido para el porcentaje de IVA.'
        }
    )

    is_active = serializers.BooleanField(
        required=False, # Es opcional, tiene un default en el modelo
        error_messages={
            'invalid': 'El valor para "activo" debe ser verdadero o falso.'
        }
    )

    # price_with_tax es un @property en el modelo, por lo tanto, es de solo lectura
    price_with_tax = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True # Este campo se calcula y no debe ser proporcionado por el cliente
    )

    class Meta:
        model = Service
        fields = '__all__' # Incluye todos los campos del modelo Service
        # read_only_fields para campos auto-gestionados
        read_only_fields = ('created_at', 'updated_at')

    # No hay validaciones cruzadas complejas en Service por ahora,
    # por lo que no necesitamos un método validate() a nivel de objeto.
    # Si quisieras, por ejemplo, que el código tuviera un formato específico
    # basado en la categoría, lo harías aquí.
