# compra/api_views.py (Este archivo NO CAMBIA respecto a la versión anterior)
from rest_framework import generics
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer # Asegúrate de que OrderItemSerializer sea el simple si lo mantienes

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