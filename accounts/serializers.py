from rest_framework import serializers
from .models import Invoice, InvoiceLine
from clients.models import Client
from logistics.models import Service

class InvoiceLineSerializer(serializers.ModelSerializer):
    service_name = serializers.ReadOnlyField(source='service.name')
    service_price = serializers.ReadOnlyField(source='service.price')
    
    class Meta:
        model = InvoiceLine
        fields = '__all__'
        read_only_fields = ('subtotal',)

class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceLineSerializer(many=True, read_only=True)
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
            
            InvoiceLine.objects.create(
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