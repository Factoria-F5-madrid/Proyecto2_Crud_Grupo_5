from rest_framework import serializers
from invoicing.models import Invoice, InvoiceItem # <--- ¡Esta es la línea CORRECTA!
from clients.models import Client
from services.models import Service
from django.contrib.auth.models import User


class InvoiceItemSerializer(serializers.ModelSerializer):
    service_name = serializers.ReadOnlyField(source='service.name')
    service_price = serializers.ReadOnlyField(source='service.price')
    
    class Meta:
        model = InvoiceItem
        fields = '__all__'
        read_only_fields = ('subtotal',)

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True, read_only=True)
    client_name = serializers.ReadOnlyField(source='client.name')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = ('invoice_number', 'total_amount', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        items_data = self.context.get('items', [])
        invoice = Invoice.objects.create(**validated_data)
        
        for item_data in items_data:
            service_id = item_data.pop('service')
            service = Service.objects.get(id=service_id)
            quantity = item_data.get('quantity', 1)
            price = item_data.get('price', service.price)
            
            InvoiceItem.objects.create(
                invoice=invoice,
                service_id=service_id,
                quantity=quantity,
                price=price,
                subtotal=quantity * price
            )
        
        # Recalcular el total de la factura
        invoice.calculate_total()
        return invoice

class InvoiceListSerializer(serializers.ModelSerializer):
    """Serializer optimizado para listados"""
    client_name = serializers.ReadOnlyField(source='client.name')
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'client_name', 'issue_date', 
                  'due_date', 'total_amount', 'status', 'status_display']
        
# Serializer para el modelo User (si lo necesitas para mostrar datos de usuario)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email') # Ajusta los campos según tus necesidades

# Serializer para el registro de nuevos usuarios
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

# Serializer para cambiar la contraseña
class ChangePasswordSerializer(serializers.Serializer):
    # Nota: Este no es un ModelSerializer porque no está mapeado directamente a un modelo para creación/actualización
    # Solo se usa para validar los campos de la contraseña.
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)