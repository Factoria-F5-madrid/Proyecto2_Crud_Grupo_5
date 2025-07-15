from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import Decimal

from clients.models import Client
from logistics.models import Service
from invoicing.models import Invoice, LineaFactura

class InvoiceAPITest(APITestCase):
    def setUp(self):
        """
        Configura los datos iniciales para todos los tests de la API de facturación.
        """
        # 1. Crear usuario para autenticación (debe tener permisos, p.ej. is_staff)
        self.user = User.objects.create_user(username='staffuser', password='testpass123', is_staff=True)
        
        # 2. Crear datos de prueba
        self.client = Client.objects.create(name="Cliente para Facturas", email="invoice@test.com")
        self.service1 = Service.objects.create(name="Diseño Web", price=Decimal("1500.00"))
        self.service2 = Service.objects.create(name="Hosting Anual", price=Decimal("100.00"))
        
        # 3. Crear una factura de prueba con sus servicios prestados
        self.invoice = Invoice.objects.create(
            client=self.client,
            issue_date=timezone.now().date(),
            due_date=timezone.now().date() + timezone.timedelta(days=30),
            status=Invoice.InvoiceStatus.DRAFT
        )
        ProvidedService.objects.create(
            invoice=self.invoice,
            service=self.service1,
            quantity=1,
            price=self.service1.price
        )
        # Actualizamos los totales de la factura
        self.invoice.calculate_totals()
        
        # 4. Definir URLs (asegúrate de que los nombres coinciden con tu urls.py)
        self.list_url = reverse('invoice-list')
        self.detail_url = reverse('invoice-detail', args=[self.invoice.id])
        
        # 5. Autenticar el cliente de la API para todas las pruebas
        self.client.force_authenticate(user=self.user)

    def test_get_invoice_list(self):
        """Prueba que se puede obtener la lista de facturas."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['client_name'], self.client.name) # Asumiendo que el serializer incluye 'client_name'

    def test_get_invoice_detail(self):
        """Prueba que se puede obtener el detalle de una factura específica."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'draft')
        self.assertEqual(Decimal(response.data['total']), self.invoice.total)

    def test_create_invoice(self):
        """
        Prueba la creación de una nueva factura con sus servicios.
        Esto asume que tu serializer acepta datos anidados para los servicios.
        """
        new_client = Client.objects.create(name="Nuevo Cliente", email="new@client.com")
        due_date_str = (timezone.now().date() + timezone.timedelta(days=15)).strftime('%Y-%m-%d')

        invoice_data = {
            "client": new_client.id,
            "due_date": due_date_str,
            "status": "draft",
            "provided_services": [ # Asumiendo que el serializer acepta una lista 'provided_services'
                {"service": self.service1.id, "quantity": 1},
                {"service": self.service2.id, "quantity": 2, "price": "90.00"} # Precio personalizado
            ]
        }
        
        response = self.client.post(self.list_url, invoice_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)
        
        # Verificar que los servicios se crearon correctamente
        new_invoice = Invoice.objects.get(id=response.data['id'])
        self.assertEqual(new_invoice.providedservice_set.count(), 2)
        
        # Verificar que el total calculado es correcto
        expected_total = (Decimal("1500.00") * 1) + (Decimal("90.00") * 2) # 1500 + 180 = 1680
        expected_total_with_tax = expected_total * (1 + (new_invoice.tax_rate / 100))
        self.assertEqual(new_invoice.total, expected_total_with_tax.quantize(Decimal('0.01')))


    def test_update_invoice_status(self):
        """Prueba la actualización del estado de una factura."""
        update_data = {'status': Invoice.InvoiceStatus.SENT}
        
        response = self.client.patch(self.detail_url, update_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, Invoice.InvoiceStatus.SENT)

    def test_delete_invoice(self):
        """Prueba la eliminación de una factura."""
        response = self.client.delete(self.detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)
        self.assertEqual(ProvidedService.objects.count(), 0) # Verificar que los servicios asociados también se borran (CASCADE)

    def test_unauthenticated_access_is_denied(self):
        """Prueba que un usuario no autenticado no puede acceder a la API."""
        self.client.force_authenticate(user=None) # Desautenticar
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)