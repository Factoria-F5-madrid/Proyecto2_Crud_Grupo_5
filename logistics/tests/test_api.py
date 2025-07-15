from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

# Importaciones para este test
from ..models import Shipment
from core.models import Category
from clients.models import Client

class ShipmentAPITest(APITestCase):
    def setUp(self):
        """Configuración para los tests de la API de envíos."""
        self.user = User.objects.create_user(username='testuser', password='testpass123', is_staff=True)
        self.client.force_authenticate(user=self.user)

        self.client_obj = Client.objects.create(legal_name="API Client", tax_id="C99999999")
        self.category_obj = Category.objects.create(name="API Category")

        self.shipment = Shipment.objects.create(
            shipment_code='API-001',
            client=self.client_obj,
            category=self.category_obj,
            recipient_name='API Recipient',
            delivery_address='789 Pine Rd',
            weight_kg='100.00',
            price='300.00'
        )

        self.list_url = reverse('shipment-list-create')
        self.detail_url = reverse('shipment-detail', args=[self.shipment.id])

    def test_get_shipment_list(self):
        """Test para obtener la lista de envíos."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_shipment(self):
        """Test para crear un nuevo envío."""
        data = {
            'shipment_code': 'API-002',
            'client': self.client_obj.id,
            'category': self.category_obj.id,
            'recipient_name': 'New Recipient',
            'delivery_address': '101 Maple Ln',
            'weight_kg': '25.00',
            'price': '99.99'
        }
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Shipment.objects.count(), 2)

    def test_delete_shipment(self):
        """Test para eliminar un envío."""
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Shipment.objects.count(), 0)