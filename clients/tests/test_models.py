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
    """"""      