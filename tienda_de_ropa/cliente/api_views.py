from rest_framework import generics
from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
import csv

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