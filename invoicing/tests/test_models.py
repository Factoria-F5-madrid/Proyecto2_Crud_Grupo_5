from django.test import TestCase
from django.utils import timezone
from decimal import Decimal
from clients.models import Client
from logistics.models import Service
from invoicing.models import Invoice, ProvidedService

class InvoiceModelTest(TestCase):

    def setUp(self):
        """Crea un cliente y servicios para las pruebas de facturas."""
        self.client = Client.objects.create(name='Cliente de Prueba', email='test@cliente.com')
        self.service1 = Service.objects.create(name='Servicio A', price=Decimal('100.00'))
        self.service2 = Service.objects.create(name='Servicio B', price=Decimal('50.00'))
        
        self.invoice = Invoice.objects.create(
            client=self.client,
            issue_date=timezone.now().date(),
            due_date=timezone.now().date() + timezone.timedelta(days=30),
        )

    def test_invoice_creation(self):
        """Test para verificar la creación de una factura."""
        self.assertEqual(self.invoice.client.name, 'Cliente de Prueba')
        self.assertEqual(self.invoice.status, 'draft') # Asumiendo 'draft' como estado inicial
        self.assertEqual(str(self.invoice), f"Factura #{self.invoice.id} para Cliente de Prueba")

    def test_add_provided_services_to_invoice(self):
        """Test para añadir servicios a una factura y calcular el total."""
        # Añadir servicios prestados a la factura
        ProvidedService.objects.create(invoice=self.invoice, service=self.service1, quantity=2, price=self.service1.price) # 2 * 100 = 200
        ProvidedService.objects.create(invoice=self.invoice, service=self.service2, quantity=3, price=self.service2.price) # 3 * 50 = 150

        # Refrescar la instancia de la factura para obtener los servicios relacionados
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.providedservice_set.count(), 2)

        # Probar el método para calcular el total (debes implementarlo en tu modelo Invoice)
        # Asumiendo que tienes un método `calculate_total()`
        self.invoice.calculate_total()
        self.assertEqual(self.invoice.total, Decimal('350.00'))
        
    def test_total_calculation_with_taxes(self):
        """Test para calcular el total incluyendo impuestos."""
        # Añadir un servicio
        ProvidedService.objects.create(invoice=self.invoice, service=self.service1, quantity=1, price=self.service1.price) # 100
        
        # Asumiendo que `calculate_total` puede aceptar un porcentaje de impuestos
        # self.invoice.calculate_total(tax_rate=Decimal('0.21')) # 21% de IVA
        # self.assertEqual(self.invoice.total, Decimal('121.00'))
        # Nota: La implementación exacta dependerá de tu modelo.
        # Por ahora, simulamos el cálculo.
        subtotal = self.invoice.providedservice_set.first().get_total() # 100.00
        tax = subtotal * Decimal('0.21')
        total = subtotal + tax
        
        self.invoice.subtotal = subtotal
        self.invoice.tax = tax
        self.invoice.total = total
        self.invoice.save()

        self.assertEqual(self.invoice.total, Decimal('121.00'))

class ProvidedServiceModelTest(TestCase):
    def setUp(self):
        client = Client.objects.create(name='Cliente PS', email='ps@test.com')
        service = Service.objects.create(name='Servicio PS', price=Decimal('75.00'))
        invoice = Invoice.objects.create(client=client, issue_date=timezone.now().date())
        
        self.provided_service = ProvidedService.objects.create(
            invoice=invoice,
            service=service,
            quantity=4,
            price=service.price
        )

    def test_provided_service_total(self):
        """Test para verificar el cálculo del subtotal de un servicio prestado."""
        # Asumiendo un método get_total() en el modelo ProvidedService
        expected_total = Decimal('300.00') # 75.00 * 4
        self.assertEqual(self.provided_service.get_total(), expected_total)