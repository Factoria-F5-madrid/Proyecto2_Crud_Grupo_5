from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Client # ¡Importa tu modelo Client (con 'Client' en mayúscula)!
import re # Importamos para validaciones de formato de NIF/CIF si es necesario

class ClientSerializer(serializers.ModelSerializer):
    # Definición explícita de campos para añadir validaciones y mensajes personalizados.
    # DRF ya toma 'required' y 'allow_blank' de los atributos blank=False/null=False del modelo.
    # Aquí los redefinimos para personalizar los mensajes de error.

    name = serializers.CharField(
        max_length=200,
        required=True,
        allow_blank=False, # El nombre no puede estar en blanco
        error_messages={
            'required': 'El nombre del cliente es obligatorio.',
            'blank': 'El nombre del cliente no puede estar en blanco.',
            'max_length': 'El nombre del cliente no puede exceder los 200 caracteres.'
        }
    )

    tax_id = serializers.CharField(
        max_length=20,
        required=True,
        allow_blank=False, # El NIF/CIF no puede estar en blanco
        validators=[
            UniqueValidator(
                queryset=Client.objects.all(),
                message="Ya existe un cliente con este NIF/CIF. Debe ser único."
            )
        ],
        error_messages={
            'required': 'El NIF/CIF es obligatorio.',
            'blank': 'El NIF/CIF no puede estar en blanco.',
            'max_length': 'El NIF/CIF no puede exceder los 20 caracteres.'
        }
    )

    address = serializers.CharField(
        max_length=255,
        required=True,
        allow_blank=False, # La dirección no puede estar en blanco
        error_messages={
            'required': 'La dirección es obligatoria.',
            'blank': 'La dirección no puede estar en blanco.',
            'max_length': 'La dirección no puede exceder los 255 caracteres.'
        }
    )

    postal_code = serializers.CharField(
        max_length=10,
        required=True,
        allow_blank=False, # El código postal no puede estar en blanco
        error_messages={
            'required': 'El código postal es obligatorio.',
            'blank': 'El código postal no puede estar en blanco.',
            'max_length': 'El código postal no puede exceder los 10 caracteres.'
        }
    )

    city = serializers.CharField(
        max_length=100,
        required=True,
        allow_blank=False, # La ciudad no puede estar en blanco
        error_messages={
            'required': 'La ciudad es obligatoria.',
            'blank': 'La ciudad no puede estar en blanco.',
            'max_length': 'La ciudad no puede exceder los 100 caracteres.'
        }
    )

    province = serializers.CharField(
        max_length=100,
        required=True,
        allow_blank=False, # La provincia no puede estar en blanco
        error_messages={
            'required': 'La provincia es obligatoria.',
            'blank': 'La provincia no puede estar en blanco.',
            'max_length': 'La provincia no puede exceder los 100 caracteres.'
        }
    )

    country = serializers.CharField(
        max_length=100,
        required=True, # Aunque tiene un default en el modelo, lo marcamos como requerido en el serializer
        allow_blank=False, # El país no puede estar en blanco
        error_messages={
            'required': 'El país es obligatorio.',
            'blank': 'El país no puede estar en blanco.',
            'max_length': 'El país no puede exceder los 100 caracteres.'
        }
    )

    email = serializers.EmailField(
        required=True,
        allow_blank=False, # El email no puede estar en blanco
        error_messages={
            'required': 'El correo electrónico es obligatorio.',
            'blank': 'El correo electrónico no puede estar en blanco.',
            'invalid': 'Por favor, introduce un formato de correo electrónico válido.'
        }
    )

    phone = serializers.CharField(
        max_length=20,
        required=True,
        allow_blank=False, # El teléfono no puede estar en blanco
        error_messages={
            'required': 'El teléfono es obligatorio.',
            'blank': 'El teléfono no puede estar en blanco.',
            'max_length': 'El teléfono no puede exceder los 20 caracteres.'
        }
    )

    contact_person = serializers.CharField(
        max_length=200,
        required=False, # Este campo es opcional (blank=True en el modelo)
        allow_blank=True, # Puede estar en blanco
        error_messages={
            'max_length': 'La persona de contacto no puede exceder los 200 caracteres.'
        }
    )

    is_active = serializers.BooleanField(
        required=False, # Es opcional, tiene un default en el modelo
        error_messages={
            'invalid': 'El valor para "activo" debe ser verdadero o falso.'
        }
    )

    notes = serializers.CharField(
        required=False, # Las notas son opcionales (blank=True en el modelo)
        allow_blank=True, # Pueden estar en blanco
        style={'base_template': 'textarea.html'}
    )

    # created_at y updated_at son auto_now_add/auto_now, no deben ser enviados por el cliente
    # Por lo tanto, no los incluimos en la definición explícita de campos aquí,
    # pero sí en Meta.fields si queremos que se muestren en las respuestas GET.

    class Meta:
        model = Client # Asegúrate de que el nombre del modelo sea 'Client'
        fields = '__all__' # Incluye todos los campos del modelo Client
        # Si prefieres ser explícito, puedes listar todos los campos:
        # fields = (
        #     'id', 'name', 'tax_id', 'address', 'postal_code', 'city',
        #     'province', 'country', 'email', 'phone', 'contact_person',
        #     'is_active', 'notes', 'created_at', 'updated_at'
        # )

    # Ejemplo de validación a nivel de campo para tax_id si necesitas un formato específico
    # (ej. NIF/CIF español)
    def validate_tax_id(self, value):
        # Este es un ejemplo simplificado. Una validación real de NIF/CIF es compleja.
        # Aquí solo verificamos que no contenga espacios y tenga una longitud mínima/máxima.
        if ' ' in value:
            raise serializers.ValidationError("El NIF/CIF no debe contener espacios.")
        if not (7 <= len(value) <= 9): # NIF/CIF suelen tener entre 7 y 9 caracteres
            raise serializers.ValidationError("El NIF/CIF debe tener entre 7 y 9 caracteres.")
        # Podrías añadir lógica más compleja aquí para validar el formato exacto (letras, números, etc.)
        # if not re.match(r'^[0-9XYZ][0-9]{7}[TRWAGMYFPDXBNJZSQVHLCKE]$', value, re.IGNORECASE):
        #     raise serializers.ValidationError("Formato de NIF/CIF inválido.")
        return value

    # Ejemplo de validación a nivel de objeto si fuera necesario.
    # Por ejemplo, si tuvieras una lógica que dependa de la combinación de ciudad y código postal.
    # def validate(self, data):
    #     city = data.get('city')
    #     postal_code = data.get('postal_code')
    #     if city == 'Madrid' and not postal_code.startswith('28'):
    #         raise serializers.ValidationError(
    #             {"postal_code": "El código postal para Madrid debe empezar con '28'."}
    #         )
    #     return data

