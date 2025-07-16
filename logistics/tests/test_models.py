from django.test import TestCase
from django.core.exceptions import ValidationError
from decimal import Decimal

# Importaciones para este test
from ..models import Shipment
from core.models import Category
from clients.models import Client

class ShipmentModelTest(TestCase):
    def setUp(self):
        """Configuración con los modelos y campos correctos."""
        self.client = Client.objects.create(legal_name="Test Client", tax_id="A12345678")
        self.category = Category.objects.create(name="National Transport")
        
        self.shipment = Shipment.objects.create(
            shipment_code='ALB-001',
            client=self.client,
            category=self.category,
            recipient_name='John Doe',
            delivery_address='123 Main St',
            weight_kg=Decimal('50.5'),
            price=Decimal('150.50')
        )

    def test_shipment_creation(self):
        """Verifica que los datos del envío se guardaron correctamente."""
        self.assertEqual(self.shipment.shipment_code, 'ALB-001')
        self.assertEqual(self.shipment.client.legal_name, "Test Client")

    def test_string_representation(self):
        """Verifica la representación en string del modelo."""
        self.assertEqual(str(self.shipment), 'ALB-001')