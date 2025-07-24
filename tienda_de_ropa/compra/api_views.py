# compra/api_views.py (Este archivo NO CAMBIA respecto a la versión anterior)
from rest_framework import generics
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer # Asegúrate de que OrderItemSerializer sea el simple si lo mantienes
from rest_framework.decorators import api_view # <--- ¡Asegúrate de que esta línea exista!
from rest_framework.response import Response # <--- Esta también es útil para vistas de API
from django.http import HttpResponse # <--- ¡AÑADE O VERIFICA ESTA LÍNEA!
import csv

# Vistas para el modelo Order (usarán el OrderSerializer anidado)
class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'pk'

# Vistas para el modelo OrderItem (Puedes mantenerlas si quieres gestionar OrderItems individualmente)
# Si solo quieres gestionar OrderItems a través de Order, podrías eliminar estas vistas
# y sus URLs, pero es útil tenerlas para flexibilidad.
class OrderItemListCreateAPIView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

class OrderItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderItem.objects.all()
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