# Proyecto2__Crud_Grupo_5/invoicing/serializers.py

from rest_framework import serializers
from .models import Invoice, InvoiceItem
from clients.models import Client
from services.models import Service
from django.utils import timezone

# Serializer para los ítems de la factura (cada línea de servicio en la factura)
class InvoiceItemSerializer(serializers.ModelSerializer):
    service = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        error_messages={
            'does_not_exist': 'El servicio con el ID proporcionado no existe.',
            'required': 'El servicio es obligatorio para el ítem de la factura.'
        }
    )

    description = serializers.CharField(
        max_length=255,
        required=False,
        allow_blank=True,
        error_messages={
            'max_length': 'La descripción del ítem no puede exceder los 255 caracteres.'
        }
    )

    quantity = serializers.IntegerField(
        min_value=1,
        required=True,
        error_messages={
            'required': 'La cantidad es obligatoria.',
            'min_value': 'La cantidad debe ser al menos 1.',
            'invalid': 'Por favor, introduce un número entero válido para la cantidad.'
        }
    )

    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        required=True,
        error_messages={
            'required': 'El precio unitario es obligatorio.',
            'min_value': 'El precio unitario debe ser mayor que cero.',
            'invalid': 'Por favor, introduce un valor numérico válido para el precio unitario.'
        }
    )

    tax_percentage = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=0.00,
        max_value=100.00,
        required=True,
        error_messages={
            'required': 'El porcentaje de IVA es obligatorio.',
            'min_value': 'El porcentaje de IVA no puede ser negativo.',
            'max_value': 'El porcentaje de IVA no puede exceder 100.',
            'invalid': 'Por favor, introduce un valor numérico válido para el porcentaje de IVA.'
        }
    )

    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = InvoiceItem
        fields = ('id', 'service', 'description', 'quantity', 'price', 'tax_percentage', 'subtotal')


# Serializer para la Factura principal
class InvoiceSerializer(serializers.ModelSerializer):
    client = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        error_messages={
            'does_not_exist': 'El cliente con el ID proporcionado no existe.',
            'required': 'El cliente es obligatorio para la factura.'
        }
    )

    invoice_number = serializers.CharField(
        read_only=True,
        max_length=50,
        error_messages={
            'max_length': 'El número de factura no puede exceder los 50 caracteres.'
        }
    )

    reference = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True,
        error_messages={
            'max_length': 'La referencia no puede exceder los 100 caracteres.'
        }
    )

    issue_date = serializers.DateField(
        required=True,
        error_messages={
            'required': 'La fecha de emisión es obligatoria.',
            'invalid': 'Por favor, introduce un formato de fecha válido (YYYY-MM-DD) para la fecha de emisión.'
        }
    )

    due_date = serializers.DateField(
        required=True,
        error_messages={
            'required': 'La fecha de vencimiento es obligatoria.',
            'invalid': 'Por favor, introduce un formato de fecha válido (YYYY-MM-DD) para la fecha de vencimiento.'
        }
    )

    total_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    tax_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    status = serializers.ChoiceField(
        choices=Invoice.STATUS_CHOICES,
        required=True,
        error_messages={
            'required': 'El estado de la factura es obligatorio.',
            'invalid_choice': 'El estado proporcionado no es válido.'
        }
    )

    notes = serializers.CharField(
        required=False,
        allow_blank=True,
        style={'base_template': 'textarea.html'}
    )

    items = InvoiceItemSerializer(many=True, required=False)

    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate(self, data):
        issue_date = data.get('issue_date')
        due_date = data.get('due_date')

        if issue_date and due_date:
            if due_date < issue_date:
                raise serializers.ValidationError(
                    {"due_date": "La fecha de vencimiento no puede ser anterior a la fecha de emisión."}
                )
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        invoice = Invoice.objects.create(**validated_data)

        for item_data in items_data:
            # service_id YA ES LA INSTANCIA DE Service GRACIAS A PrimaryKeyRelatedField
            service_instance = item_data.pop('service') # <-- ¡CORRECCIÓN CLAVE AQUÍ!
            InvoiceItem.objects.create(invoice=invoice, service=service_instance, **item_data)

        # Recalcula el total de la factura después de añadir los ítems
        invoice.calculate_total()
        invoice.save() # Asegurarse de guardar la factura después de calcular totales

        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)

        # Actualiza los campos de la factura principal
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if items_data is not None:
            instance.items.all().delete() # Elimina todos los ítems existentes
            for item_data in items_data:
                # service_id YA ES LA INSTANCIA DE Service GRACIAS A PrimaryKeyRelatedField
                service_instance = item_data.pop('service') # <-- ¡CORRECCIÓN CLAVE AQUÍ!
                InvoiceItem.objects.create(invoice=instance, service=service_instance, **item_data)

            # Recalcula el total de la factura después de actualizar/recrear los ítems
            instance.calculate_total()
            instance.save() # Asegurarse de guardar la factura después de calcular totales

        return instance

