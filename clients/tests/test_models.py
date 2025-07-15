from django.test import TestCase
from clients.models import Client
from django.core.exceptions import ValidationError

class ClientModelTest(TestCase):
    def setUp(self):
        """Configuración inicial para cada test de Client"""
        self.client_data = {
            'name' : 'Empresa ABC',
            'email': 'contacto@abc.com',
            'phone': '912345678',
            'address': 'Calle Principal 123, Madrid',
            'tax_id': 'B12345678'
        }
        self.test_client = Client.objects.create(**self.client_data)

    def test_client_creation(self):
        """Test para verificar la creación correcta de un cliente"""
        self.assertEqual(self.test_client.name, 'Empresa ABC')
        self.assertEqual(self.test_client.email, 'contacto@abc.com')
        self.assertEqual(self.test_client.phone, '912345678')
        self.assertEqual(self.test_client.address, 'Calle Principal 123, Madrid')
        self.assertEqual(self.test_client.tax_id, 'B12345678')
        # Verifica que los clientes están activos por defectos
        self.assertTrue(self.test_client.is_active)
    
    def test_String_representation(self):
        """Test para verficar la representación en string del modelo"""
        self.assertEqual(str(self.test_client), 'Empresa ABC')
        
    def test_email_validation(self):
        """Test para verificar la validación del formato de email"""
        # Crear cliente con email inválido
        invalid_client = Client(
            name='Cliente Test',
            email='email-inválido', # Email inválido
            phone='912345678'
        )
        
        # Verificar que se lanza validationError al validar
        with self.assertRaises(ValidationError):
            invalid_client.full_clean()

class ClientFilterTest(TestCase):
    """Tests para verificar los filtros de clientes"""
    
    def setUp(self):
        """Crear varios clientes para probar los filtros"""
        Client.objects.create(
            name='Cliente Activo',
            email='activo@test.com',
            phone='912345678',
            is_active=True
        )    
        
        Client.objects.create(
            name='Cliente Inactivo',
            email='inactivo@test.com',
            phone='922222222',
            is_active=False
        )
        
        Client.objects.create(
            name='Otro Cliente',
            email='otro@test.com',
            phone='933333333',
            is_active=True
        )
        
    def test_filter_active_clients(self):
        """Test para verficar el filtrado de clientes activos"""
        active_clients = Client.objects.filter(is_active=True)
        self.assertEqual(active_clients.count(), 2)
        
    def test_filter_by_name(self):
        """Test para verificar la búsqueda de clientes por nombre"""
        filtered_clients = client.objects.filter(name__contains='Activo')
        self.assertEqual(filtered_clients.count(), 1)
        self.assertEqual(filtered_clients[0].email, 'activo@test.com')

        