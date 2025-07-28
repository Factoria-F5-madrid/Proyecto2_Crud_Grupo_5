import csv
from io import StringIO
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import datetime, timedelta

# Importa tus modelos y serializadores reales
from cliente.models import Customer
from cliente.serializers import CustomerSerializer


class CustomerAPITests(APITestCase):
    """
    Clase de tests para las vistas de la API de Clientes.
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Configura datos de prueba que se ejecutarán una vez para toda la clase de test.
        """
        cls.customer1 = Customer.objects.create(
            name='Juan Pérez', 
            email='juan.perez@example.com', 
            phone='111-222-3333'
            # 'created_at' se llena automáticamente con auto_now_add=True
        )
        cls.customer2 = Customer.objects.create(
            name='Ana García', 
            email='ana.garcia@example.com', 
            phone='444-555-6666'
        )
        cls.customer3 = Customer.objects.create(
            name='Carlos Ruíz', 
            email='carlos.ruiz@example.com', 
            phone='777-888-9999'
        )

        # Ajustar 'created_at' para propósitos de ordenamiento de forma programática
        # (Esto no se hace en un setUp normal, pero es útil para tests específicos de orden)
        # Nota: En un entorno de producción, auto_now_add=True solo se establece al crear.
        # Para forzar un orden específico en tests, a veces se manipula así o se crean en un orden específico.
        # Aquí, para simplificar, asumimos que se crearon en un orden que permite la prueba de -created_at
        # de la vista. Si auto_now_add=True te causa problemas para establecerlo en los tests,
        # considera eliminar auto_now_add=True y manejar la fecha manualmente o en el serializador.
        # Para la prueba, el orden de creación debería ser suficiente para el ordenamiento por defecto.
        # Sin embargo, para fechas exactas de prueba, a veces se requiere crear objetos con mock de datetime o setters.

    def test_list_customers(self):
        """
        Verifica que la vista GET /api/customers/ lista todos los clientes.
        """
        url = reverse('cliente_api:customer-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        
        # Verificar el ordenamiento por defecto (-created_at)
        # Dado que se crearon en orden customer1, customer2, customer3
        # y created_at es auto_now_add, customer3 será el más reciente.
        self.assertEqual(response.data[0]['name'], self.customer3.name) 
        self.assertEqual(response.data[1]['name'], self.customer2.name) # Orden actual de creación
        self.assertEqual(response.data[2]['name'], self.customer1.name) # Orden actual de creación

    def test_create_customer_success(self):
        """
        Verifica la creación exitosa de un nuevo cliente via POST.
        """
        url = reverse('cliente_api:customer-list-create')
        new_customer_data = {
            'name': 'María López', 
            'email': 'maria.lopez@example.com', 
            'phone': '000-111-2222'
        }
        
        response = self.client.post(url, new_customer_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Customer.objects.filter(email='maria.lopez@example.com').exists())
        self.assertEqual(response.data['name'], 'María López')
        # Verificar que created_at se genera automáticamente y no está vacío