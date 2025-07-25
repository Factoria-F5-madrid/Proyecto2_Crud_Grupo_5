from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
import csv
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from django_filters import rest_framework as django_filters

class OrderFilter(django_filters.FilterSet):
    """Custom filter for orders"""
    order_date_from = django_filters.DateTimeFilter(field_name="order_date", lookup_expr='gte')
    order_date_to = django_filters.DateTimeFilter(field_name="order_date", lookup_expr='lte')
    total_min = django_filters.NumberFilter(field_name="total_amount", lookup_expr='gte')
    total_max = django_filters.NumberFilter(field_name="total_amount", lookup_expr='lte')
    
    class Meta:
        model = Order
        fields = {
            'customer': ['exact'],
            'status': ['exact'],
        }

class OrderListCreateAPIView(generics.ListCreateAPIView):
    """
    Vista para listar todos los pedidos o crear uno nuevo.
    - GET /api/orders/ (Lista todos los pedidos con filtros)
    - POST /api/orders/ (Crea un nuevo pedido con items anidados)
    
    Filtros disponibles:
    - ?customer=1 (filtra por cliente)
    - ?status=PENDIENTE (filtra por estado)
    - ?order_date_from=2023-01-01&order_date_to=2023-12-31 (rango de fechas)
    - ?total_min=100&total_max=500 (rango de totales)
    - ?ordering=-order_date (ordena por campos)
    """
    queryset = Order.objects.all().select_related('customer').prefetch_related('items__product')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = OrderFilter
    ordering_fields = ['order_date', 'total_amount']
    ordering = ['-order_date']
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista para recuperar, actualizar o eliminar un pedido específico.
    - GET /api/orders/{id}/ (Obtiene los detalles de un pedido)
    - PUT /api/orders/{id}/ (Actualiza un pedido completo)
    - PATCH /api/orders/{id}/ (Actualiza parcialmente un pedido)
    - DELETE /api/orders/{id}/ (Elimina un pedido)
    """
    queryset = Order.objects.all().select_related('customer').prefetch_related('items__product')
    serializer_class = OrderSerializer
    lookup_field = 'pk'
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderItemListCreateAPIView(generics.ListCreateAPIView):
    """
    Vista opcional para gestionar OrderItems individualmente.
    Filtros por pedido: ?order=1
    """
    queryset = OrderItem.objects.all().select_related('order', 'product')
    serializer_class = OrderItemSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['order', 'product']
    ordering = ['id']

class OrderItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista opcional para gestionar un OrderItem específico.
    """
    queryset = OrderItem.objects.all().select_related('order', 'product')
    serializer_class = OrderItemSerializer
    lookup_field = 'pk'

@api_view(['GET'])
def export_orders_csv_api(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pedidos.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID Pedido', 'ID Cliente', 'Nombre Cliente', 'Fecha Pedido'])

    orders = Order.objects.all().order_by('id')
    for order in orders:
        customer_name = order.customer.name if order.customer else ''
        writer.writerow([
            order.id,
            order.customer.id,
            customer_name,
            order.order_date.strftime('%Y-%m-%d %H:%M:%S')
        ])
    return response

@api_view(['GET'])
def export_order_items_csv_api(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="articulos_pedido.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID Item', 'ID Pedido', 'ID Producto', 'Nombre Producto', 'Cantidad'])

    order_items = OrderItem.objects.all().order_by('id')
    for item in order_items:
        product_name = item.product.name if item.product else ''
        writer.writerow([
            item.id,
            item.order.id,
            item.product.id,
            product_name,
            item.quantity
        ])
    return response