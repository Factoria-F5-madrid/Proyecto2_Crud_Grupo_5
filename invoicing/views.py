from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Invoice, InvoiceLine
from .serializers import InvoiceSerializer, InvoiceLineSerializer, InvoiceListSerializer
import datetime
from decimal import Decimal
from clients.models import Client
from logistics.models import Shipment

class InvoiceListCreate(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    filterset_fields = ['client', 'status', 'issue_date']
    search_fields = ['invoice_number', 'client__name']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['issue_date', 'due_date', 'total_amount']
    ordering = ['-issue_date']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return InvoiceListSerializer
        return InvoiceSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        items_data = request.data.get('items', [])
        
        serializer.context['items'] = items_data
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class InvoiceRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

class InvoiceLineCreate(generics.CreateAPIView):
    serializer_class = InvoiceLineSerializer

    def perform_create(self, serializer):
        invoice_id = self.kwargs.get('invoice_id')
        invoice = get_object_or_404(Invoice, id=invoice_id)
        serializer.save(invoice=invoice)
        invoice.calculate_total()

class InvoiceLineRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvoiceLineSerializer
    
    def get_queryset(self):
        invoice_id = self.kwargs.get('invoice_id')
        return InvoiceLine.objects.filter(invoice_id=invoice_id)

    def perform_update(self, serializer):
        serializer.save()
        invoice_id = self.kwargs.get('invoice_id')
        invoice = get_object_or_404(Invoice, id=invoice_id)
        invoice.calculate_total()

    def perform_destroy(self, instance):
        invoice = instance.invoice
        instance.delete()
        invoice.calculate_total()

class InvoiceStatusUpdate(APIView):
    def patch(self, request, pk):
        invoice = get_object_or_404(Invoice, pk=pk)
        status_value = request.data.get('status')
        
        if status_value is not None:
            invoice.status = status_value
            invoice.save()
            serializer = InvoiceSerializer(invoice)
            return Response(serializer.data)
        
        return Response(
            {"error": "Status not provided"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

class GenerateInvoicePDF(APIView):
    def get(self, request, pk):
        # Esta es una implementación básica. En un proyecto real,
        # aquí generarías el PDF real y lo devolverías.
        invoice = get_object_or_404(Invoice, pk=pk)
        
        # Simulando la generación de PDF
        return Response({
            "message": f"PDF para factura {invoice.invoice_number} generado exitosamente",
            "invoice_id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "client": invoice.client.name,
            "total": str(invoice.total_amount),
            "generated_at": datetime.datetime.now().isoformat()
        })

@api_view(['POST']) # Usamos POST porque esta acción crea un nuevo recurso (una factura)
@permission_classes([IsAdminUser]) # Solo administradores o personal pueden generar facturas
def generate_client_invoice_view(request, client_id):
    """
    Crea una factura para un cliente específico a partir de todos sus
    envíos completados y no facturados.
    """
    # 1. Obtener el cliente
    client = get_object_or_404(Client, id=client_id)

    # 2. Encontrar los envíos pendientes de facturar para este cliente
    shipments_to_invoice = Shipment.objects.filter(
        client=client, 
        is_invoiced=False
    )

    if not shipments_to_invoice.exists():
        return Response(
            {"detail": "No hay envíos pendientes de facturar para este cliente."},
            status=status.HTTP_404_NOT_FOUND
        )

    # 3. Crear la cabecera de la factura
    new_invoice = Invoice.objects.create(
        client=client,
        invoice_number=f"F2025-{Invoice.objects.count() + 1}", # Lógica simple para el nº de factura
        due_date=timezone.now().date() + timezone.timedelta(days=client.payment_term.due_days),
        # Aquí puedes añadir la lógica de exención de IVA si aplica al cliente
        # is_vat_exempt=client.is_export_client, 
    )

    # 4. Crear una línea de factura por cada envío
    for shipment in shipments_to_invoice:
        InvoiceLine.objects.create(
            invoice=new_invoice,
            shipment=shipment,
            description=f"Transporte a {shipment.recipient_name} (Albarán: {shipment.shipment_code})",
            amount=shipment.price
        )
        # Marcar el envío como facturado para no volver a incluirlo
        shipment.is_invoiced = True
        shipment.save()

    # 5. Calcular los totales finales de la factura
    new_invoice.calculate_totals()
    new_invoice.save()
    
    # 6. Devolver la factura recién creada
    serializer = InvoiceSerializer(new_invoice)
    return Response(serializer.data, status=status.HTTP_201_CREATED)