from rest_framework import generics
from .models import Customer
from .serializers import CustomerSerializer

class CustomerListCreateAPIView(generics.ListCreateAPIView):
    """
    Vista de API para listar todos los clientes o crear uno nuevo.
    - GET /api/customers/ (Lista todos los clientes)
    - POST /api/customers/ (Crea un nuevo cliente)
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class CustomerRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Vista de API para recuperar, actualizar o eliminar un cliente específico.
    - GET /api/customers/{id}/ (Obtiene los detalles de un cliente)
    - PUT /api/customers/{id}/ (Actualiza un cliente existente)
    - PATCH /api/customers/{id}/ (Actualiza parcialmente un cliente existente)
    - DELETE /api/customers/{id}/ (Elimina un cliente)
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = 'pk' # Usa 'pk' (clave primaria) para buscar el objeto