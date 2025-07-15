from rest_framework import serializers
from invoicing.models import Invoice
from clients.models import Client
from logistics.models import Shipment

class DashboardSummarySerializer(serializers.Serializer):
    total_clients = serializers.IntegerField()
    active_clients = serializers.IntegerField()
    total_services = serializers.IntegerField()
    total_invoices = serializers.IntegerField()
    invoices_pending = serializers.IntegerField()
    invoices_paid = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    pending_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

class MonthlySalesSerializer(serializers.Serializer):
    month = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    count = serializers.IntegerField()

class TopClientSerializer(serializers.ModelSerializer):
    total_invoiced = serializers.DecimalField(max_digits=10, decimal_places=2)
    invoices_count = serializers.IntegerField()
    
    class Meta:
        model = Client
        fields = ['id', 'name', 'total_invoiced', 'invoices_count']

class TopServiceSerializer(serializers.ModelSerializer):
    times_invoiced = serializers.IntegerField()
    total_invoiced = serializers.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        model = Shipment
        fields = ['id', 'name', 'times_invoiced', 'total_invoiced']