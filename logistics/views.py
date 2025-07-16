from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Shipment
from core.models import Category
from .serializers import ShipmentSerializer, ShipmentListSerializer, CategorySerializer

# --- Vistas para Category ---

class CategoryListCreate(generics.ListCreateAPIView):
    """
    API view to list and create Categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    ordering = ['name']

class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, and destroy a Category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# --- Vistas para Shipment ---

class ShipmentListCreate(generics.ListCreateAPIView):
    """
    API view to list and create Shipments.
    """
    queryset = Shipment.objects.all()
    
    # --- CAMPOS CORREGIDOS ---
    # Usamos los campos que sí existen en el modelo Shipment
    filterset_fields = ['client', 'is_invoiced']
    search_fields = ['shipment_code', 'recipient_name', 'client__legal_name']
    ordering_fields = ['created_at', 'price']
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Usa un serializador detallado para la lista (GET)
        y uno más simple para la creación (POST).
        """
        if self.request.method == 'GET':
            return ShipmentListSerializer
        return ShipmentSerializer

class ShipmentRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, and destroy a Shipment.
    """
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer