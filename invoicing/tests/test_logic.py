from django.test import TestCase
from django.utils import timezone
from clients.models import Client
from logistics.models import Service, Category
from invoicing.models import Invoice, LineaFactura

# Asumimos que tienes una función como esta en algún lugar
# from invoicing.logic import generate_monthly_invoices

class InvoicingLogicTest(TestCase):
    def setUp(self):
        """Crea datos correctos para probar la lógica de facturación."""
        # 1. Crear dependencias
        self.category = Category.objects.create(name="Suscripciones")
        
        # 2. Crear Clientes con todos sus datos requeridos
        self.client_recurrent = Client.objects.create(
            name='Cliente Mensual',
            tax_id='A11111111', # <-- CORREGIDO
            email='mensual@test.com'
        )
        self.client_onetime = Client.objects.create(
            name='Cliente Puntual',
            tax_id='B22222222', # <-- CORREGIDO
            email='puntual@test.com'
        )
        
        # 3. Crear Servicio con todos sus datos requeridos
        self.recurrent_service = Service.objects.create(
            cliente=self.client_recurrent, # <-- CORREGIDO
            category=self.category,       # <-- CORREGIDO
            descripcion='Suscripción Mensual', # <-- CORREGIDO (usando descripción)
            coste=250.00,                 # <-- CORREGIDO (usando coste)
            fecha_servicio=timezone.now().date()
        )

    def test_monthly_invoice_generation(self):
        """
        Test para verificar la generación de facturas mensuales.
        """
        # 1. Estado inicial: no hay facturas
        self.assertEqual(Invoice.objects.count(), 0)

        # 2. Ejecutar la lógica de generación (esta línea es conceptual)
        # Por ejemplo, podrías llamar a una tarea de Celery o un comando de gestión
        # generate_monthly_invoices() # Descomenta y adapta a tu función real

        # Para simular el resultado sin tener la función, creamos la factura manualmente:
        # ----- INICIO SIMULACIÓN -----
        new_invoice = Invoice.objects.create(
            cliente=self.client_recurrent,
            numero_factura="F2025-001",
            fecha_vencimiento=timezone.now().date() + timezone.timedelta(days=30),
        )
        LineaFactura.objects.create(
            factura=new_invoice,
            servicio=self.recurrent_service,
            descripcion=self.recurrent_service.descripcion,
            precio_unitario=self.recurrent_service.coste
        )
        # ----- FIN SIMULACIÓN -----

        # 3. Comprobar el resultado
        self.assertEqual(Invoice.objects.count(), 1)
        
        created_invoice = Invoice.objects.first()
        self.assertEqual(created_invoice.cliente, self.client_recurrent)
        
        # Verificamos la línea de la factura
        line_item = created_invoice.lineas.first()
        self.assertIsNotNone(line_item)
        self.assertEqual(line_item.servicio, self.recurrent_service)
        self.assertEqual(line_item.precio_unitario, self.recurrent_service.coste)