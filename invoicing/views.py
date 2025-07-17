from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Invoice, InvoiceItem
# invoicing/views.py
from .serializers import InvoiceSerializer, InvoiceItemSerializer 
import datetime

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

class InvoiceItemCreate(generics.CreateAPIView):
    serializer_class = InvoiceItemSerializer

    def perform_create(self, serializer):
        invoice_id = self.kwargs.get('invoice_id')
        invoice = get_object_or_404(Invoice, id=invoice_id)
        serializer.save(invoice=invoice)
        invoice.calculate_total()

class InvoiceItemRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvoiceItemSerializer
    
    def get_queryset(self):
        invoice_id = self.kwargs.get('invoice_id')
        return InvoiceItem.objects.filter(invoice_id=invoice_id)

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