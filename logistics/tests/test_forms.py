from django.test import TestCase

from ..forms import Shipment
from core.models import Category
from clients.models import Client

class ShipmentFormTest(TestCase):
    def setUp(self):
        """Crea las dependencias necesarias para el formulario."""
        self.client = Client.objects.create(legal_name="Form Client", tax_id="B87654321")
        self.category = Category.objects.create(name="International")

    def test_valid_form(self):
        """Prueba que el formulario es válido con datos correctos."""
        data = {
            'shipment_code': 'ALB-002',
            'client': self.client.id,
            'category': self.category.id,
            'recipient_name': 'Jane Smith',
            'delivery_address': '456 Oak Ave',
            'weight_kg': '75.00',
            'price': '200.00'
        }
        form = Shipment(data=data)
        self.assertTrue(form.is_valid(), form.errors)

    def test_form_is_invalid_if_required_field_is_missing(self):
        """Prueba que el formulario es inválido si falta un campo requerido."""
        data = {'shipment_code': 'ALB-003'} # Faltan campos requeridos
        form = Shipment(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('client', form.errors)
        self.assertIn('price', form.errors)