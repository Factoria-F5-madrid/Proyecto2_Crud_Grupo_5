from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, F, Q
from django.db.models.functions import TruncMonth
from datetime import datetime, timedelta
from .serializers import (
    DashboardSummarySerializer, 
    MonthlySalesSerializer,
    TopClientSerializer,
    TopServiceSerializer
)
from clients.models import Client
from services.models import Service
from invoicing.models import Invoice, InvoiceItem

class DashboardSummaryView(APIView):
    def get(self, request):
        # Obtener datos para el resumen del dashboard
        total_clients = Client.objects.count()
        active_clients = Client.objects.filter(is_active=True).count()
        total_services = Service.objects.count()
        total_invoices = Invoice.objects.count()
        invoices_pending = Invoice.objects.filter(status='pending').count()
        invoices_paid = Invoice.objects.filter(status='paid').count()
        total_amount = Invoice.objects.aggregate(total=Sum('total_amount'))['total'] or 0
        pending_amount = Invoice.objects.filter(status='pending').aggregate(
            total=Sum('total_amount'))['total'] or 0
        
        data = {
            'total_clients': total_clients,
            'active_clients': active_clients,
            'total_services': total_services,
            'total_invoices': total_invoices,
            'invoices_pending': invoices_pending,
            'invoices_paid': invoices_paid,
            'total_amount': total_amount,
            'pending_amount': pending_amount
        }
        
        serializer = DashboardSummarySerializer(data)
        return Response(serializer.data)

class MonthlySalesView(APIView):
    def get(self, request):
        # Obtener datos de ventas mensuales del último año
        year_ago = datetime.now() - timedelta(days=365)
        
        monthly_sales = Invoice.objects.filter(
            issue_date__gte=year_ago
        ).annotate(
            month=TruncMonth('issue_date')
        ).values(
            'month'
        ).annotate(
            total=Sum('total_amount'),
            count=Count('id')
        ).order_by('month')
        
        # Convertir los resultados al formato esperado por el serializer
        formatted_data = []
        for entry in monthly_sales:
            formatted_data.append({
                'month': entry['month'].strftime('%Y-%m'),
                'total': entry['total'],
                'count': entry['count']
            })
        
        serializer = MonthlySalesSerializer(formatted_data, many=True)
        return Response(serializer.data)

class TopClientsView(APIView):
    def get(self, request):
        # Obtener los clientes con mayor facturación
        limit = int(request.query_params.get('limit', 5))
        
        top_clients = Client.objects.annotate(
            total_invoiced=Sum('invoice__total_amount'),
            invoices_count=Count('invoice')
        ).filter(
            total_invoiced__isnull=False
        ).order_by('-total_invoiced')[:limit]
        
        serializer = TopClientSerializer(top_clients, many=True)
        return Response(serializer.data)

class TopServicesView(APIView):
    def get(self, request):
        # Obtener los servicios más facturados
        limit = int(request.query_params.get('limit', 5))
        
        top_services = Service.objects.annotate(
            times_invoiced=Count('invoiceitem'),
            total_invoiced=Sum(F('invoiceitem__price') * F('invoiceitem__quantity'))
        ).filter(
            times_invoiced__gt=0
        ).order_by('-times_invoiced')[:limit]
        
        serializer = TopServiceSerializer(top_services, many=True)
        return Response(serializer.data)