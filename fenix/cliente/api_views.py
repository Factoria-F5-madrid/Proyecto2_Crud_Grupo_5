from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
import csv
from .models import Customer
from .serializers import CustomerSerializer

class CustomerListCreateAPIView(generics.ListCreateAPIView):
    """
    Vista de API para listar todos los clientes o crear uno nuevo.
    - GET /api/customers/ (Lista todos los clientes con filtros y búsqueda)
    - POST /api/customers/ (Crea un nuevo cliente)
    
    Filtros disponibles:
    - ?search=nombre (busca en nombre y email)
    - ?ordering=name,-created_at (ordena por campos)
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['name', 'email', 'created_at']
    ordering = ['-created_at']  # Orden por defecto
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
    lookup_field = 'pk'
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def export_customers_csv_api(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clientes.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Nombre', 'Correo Electronico', 'Telefono', 'Fecha Registro'])

    customers = Customer.objects.all().order_by('id')
    for customer in customers:
        writer.writerow([
            customer.id,
            customer.name,
            customer.email,
            customer.phone,
            customer.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])
    return response