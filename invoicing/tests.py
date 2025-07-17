from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model # Importa el modelo de usuario
from .models import Invoice, InvoiceItem
from clients.models import Client
from services.models import Service, ServiceCategory
from datetime import date, timedelta

User = get_user_model() # Obtener el modelo de usuario activo

class InvoiceTests(APITestCase):
    """
    Clase de tests para el modelo Invoice, incluyendo la creación/actualización de InvoiceItems anidados.
    """

    def setUp(self):
        # Crear un usuario para autenticar las peticiones
        self.user = User.objects.create_user(username='testadmin', password='TestPassword123')
        # Autenticar el cliente de test
        self.client.force_authenticate(user=self.user) # <-- ¡Esta es la línea clave para autenticación!

        # URL para la lista de facturas (POST para crear, GET para listar)
        self.invoice_list_url = reverse('invoice-list-create')
        # URL para una factura específica (GET, PUT, PATCH, DELETE por ID)
        self.invoice_detail_url = lambda pk: reverse('invoice-detail', kwargs={'pk': pk})
        # URL para crear ítems de factura asociados a una factura específica (si se usan directamente)
        self.invoice_item_create_url = lambda invoice_id: reverse('invoice-item-create', kwargs={'invoice_id': invoice_id})
        # URL para un ítem de factura específico asociado a una factura (si se usan directamente)
        self.invoice_item_detail_url = lambda invoice_id, pk: reverse('invoice-item-detail', kwargs={'invoice_id': invoice_id, 'pk': pk})
        # URL para actualizar el estado de la factura (si se usa directamente)
        self.invoice_status_update_url = lambda pk: reverse('invoice-status-update', kwargs={'pk': pk})


        # Crear un cliente y servicios para usar en los tests de factura
        self.client_obj = Client.objects.create(
            name='Cliente Factura S.A.', tax_id='B98765432', address='Av. Principal 1',
            postal_code='28002', city='Madrid', province='Madrid', country='España',
            email='facturas@cliente.com', phone='912345670'
        )
        self.service_category = ServiceCategory.objects.create(name='Software', description='Desarrollo de software')
        self.service_obj = Service.objects.create(
            name='Licencia Software', code='LIC001', category=self.service_category, # Pasa la instancia de category
            price='500.00', tax_percentage='21.00'
        )
        self.service_obj_2 = Service.objects.create(
            name='Soporte Anual', code='SOP001', category=self.service_category, # Pasa la instancia de category
            price='200.00', tax_percentage='10.00'
        )

        # Datos base para una factura válida con ítems
        self.valid_invoice_data = {
            'client': self.client_obj.pk, # Para el serializer, se espera el PK del cliente
            'issue_date': str(date.today()),
            'due_date': str(date.today() + timedelta(days=30)),
            'status': 'pending',
            'notes': 'Factura de prueba con ítems.',
            'items': [
                {
                    'service': self.service_obj.pk, # Para el serializer, se espera el PK del servicio
                    'description': 'Licencia de software anual',
                    'quantity': 1,
                    'price': '500.00',
                    'tax_percentage': '21.00'
                },
                {
                    'service': self.service_obj_2.pk, # Para el serializer, se espera el PK del servicio
                    'description': 'Servicio de soporte por 1 año',
                    'quantity': 2,
                    'price': '200.00',
                    'tax_percentage': '10.00'
                }
            ]
        }

    # --- Tests de Creación (POST) ---

    def test_create_invoice_success_with_items(self):
        """
        Verifica que se puede crear una factura exitosamente con ítems anidados.
        """
        response = self.client.post(self.invoice_list_url, self.valid_invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        invoice = Invoice.objects.get()
        self.assertEqual(invoice.client, self.client_obj)
        self.assertEqual(invoice.items.count(), 2) # Verifica que se crearon los 2 ítems

        # Verifica que los totales se calcularon correctamente (puede haber pequeñas diferencias de float)
        # Item 1: 1 * 500 = 500
        # Item 2: 2 * 200 = 400
        # total_amount = 500 + 400 = 900
        # tax_amount = (500 * 0.21) + (400 * 0.10) = 105 + 40 = 145
        self.assertAlmostEqual(float(invoice.total_amount), 900.00)
        self.assertAlmostEqual(float(invoice.tax_amount), 145.00)


    def test_create_invoice_success_no_items(self):
        """
        Verifica que se puede crear una factura sin ítems inicialmente.
        """
        data = self.valid_invoice_data.copy()
        data.pop('items') # No enviar ítems
        response = self.client.post(self.invoice_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        invoice = Invoice.objects.get()
        self.assertEqual(invoice.items.count(), 0) # No se crearon ítems
        self.assertEqual(float(invoice.total_amount), 0.00) # Total debe ser 0 si no hay ítems
        self.assertEqual(float(invoice.tax_amount), 0.00) # IVA debe ser 0 si no hay ítems

    def test_create_invoice_no_client(self):
        """
        Verifica que la creación falla si no se proporciona el cliente.
        """
        data = self.valid_invoice_data.copy()
        data.pop('client')
        response = self.client.post(self.invoice_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('client', response.data)
        self.assertIn('El cliente es obligatorio para la factura.', response.data['client'])

    def test_create_invoice_non_existent_client(self):
        """
        Verifica que la creación falla si el cliente no existe.
        """
        data = self.valid_invoice_data.copy()
        data['client'] = 9999 # ID de cliente que no existe
        response = self.client.post(self.invoice_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('client', response.data)
        self.assertIn('El cliente con el ID proporcionado no existe.', response.data['client'])

    def test_create_invoice_due_date_before_issue_date(self):
        """
        Verifica que la creación falla si la fecha de vencimiento es anterior a la de emisión.
        """
        data = self.valid_invoice_data.copy()
        data['issue_date'] = str(date.today())
        data['due_date'] = str(date.today() - timedelta(days=1)) # Fecha de vencimiento en el pasado
        response = self.client.post(self.invoice_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('due_date', response.data)
        self.assertIn('La fecha de vencimiento no puede ser anterior a la fecha de emisión.', response.data['due_date'])

    def test_create_invoice_invalid_status(self):
        """
        Verifica que la creación falla si el estado no es válido.
        """
        data = self.valid_invoice_data.copy()
        data['status'] = 'invalid_status'
        response = self.client.post(self.invoice_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('status', response.data)
        self.assertIn('El estado proporcionado no es válido.', response.data['status'])

    # --- Tests de validación de ítems anidados (a través de la creación/actualización de la factura) ---

    def test_create_invoice_item_invalid_quantity(self):
        """
        Verifica que la creación de factura falla si un ítem tiene cantidad inválida (ej. 0 o negativa).
        """
        data = self.valid_invoice_data.copy()
        data['items'][0]['quantity'] = 0 # Cantidad inválida
        response = self.client.post(self.invoice_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('items', response.data)
        self.assertIn('quantity', response.data['items'][0])
        self.assertIn('La cantidad debe ser al menos 1.', response.data['items'][0]['quantity'])

    def test_create_invoice_item_negative_price(self):
        """
        Verifica que la creación de factura falla si un ítem tiene precio negativo.
        """
        data = self.valid_invoice_data.copy()
        data['items'][0]['price'] = '-50.00' # Precio inválido
        response = self.client.post(self.invoice_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('items', response.data)
        self.assertIn('price', response.data['items'][0])
        self.assertIn('El precio unitario debe ser mayor que cero.', response.data['items'][0]['price'])

    def test_create_invoice_item_tax_percentage_out_of_range(self):
        """
        Verifica que la creación de factura falla si un ítem tiene porcentaje de IVA fuera de rango.
        """
        data = self.valid_invoice_data.copy()
        data['items'][0]['tax_percentage'] = '150.00' # IVA fuera de rango
        response = self.client.post(self.invoice_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('items', response.data)
        self.assertIn('tax_percentage', response.data['items'][0])
        self.assertIn('El porcentaje de IVA no puede exceder 100.', response.data['items'][0]['tax_percentage'])

    def test_create_invoice_item_non_existent_service(self):
        """
        Verifica que la creación de factura falla si un ítem referencia un servicio inexistente.
        """
        data = self.valid_invoice_data.copy()
        data['items'][0]['service'] = 9999 # Servicio inexistente
        response = self.client.post(self.invoice_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('items', response.data)
        self.assertIn('service', response.data['items'][0])
        self.assertIn('El servicio con el ID proporcionado no existe.', response.data['items'][0]['service'])


    # --- Tests de Actualización (PUT/PATCH) ---

    def test_update_invoice_success_update_items(self):
        """
        Verifica que se puede actualizar una factura y sus ítems exitosamente.
        """
        # Crear una factura inicial
        initial_data = self.valid_invoice_data.copy()
        initial_data['items'] = [self.valid_invoice_data['items'][0]] # Solo un ítem inicialmente
        response = self.client.post(self.invoice_list_url, initial_data, format='json')
        # Asegúrate de que la creación inicial fue exitosa antes de continuar
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        invoice = Invoice.objects.get(pk=response.data['id'])
        self.assertEqual(invoice.items.count(), 1)

        # Datos para actualizar: cambiar un ítem y añadir otro
        updated_items_data = [
            {
                'service': self.service_obj.pk,
                'description': 'Licencia de software actualizada',
                'quantity': 2, # Cantidad cambiada
                'price': '500.00',
                'tax_percentage': '21.00'
            },
            {
                'service': self.service_obj_2.pk, # Nuevo ítem
                'description': 'Soporte Adicional',
                'quantity': 1,
                'price': '300.00',
                'tax_percentage': '10.00'
            }
        ]
        updated_invoice_data = {
            'client': self.client_obj.pk,
            'issue_date': str(date.today()),
            'due_date': str(date.today() + timedelta(days=45)), # Fecha de vencimiento cambiada
            'status': 'paid', # Estado cambiado
            'notes': 'Factura actualizada con nuevos ítems.', # Añadir notas para asegurar que no se pierden
            'items': updated_items_data
        }

        response = self.client.put(self.invoice_detail_url(invoice.pk), updated_invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) # <-- ¡CORRECCIÓN AQUÍ! Esperar 200 OK
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, 'paid')
        self.assertEqual(invoice.items.count(), 2) # Ahora debe tener 2 ítems

        # Verificar los nuevos totales
        # Item 1: 2 * 500 = 1000
        # Item 2: 1 * 300 = 300
        # total_amount = 1000 + 300 = 1300
        # tax_amount = (1000 * 0.21) + (300 * 0.10) = 210 + 30 = 240
        self.assertAlmostEqual(float(invoice.total_amount), 1300.00)
        self.assertAlmostEqual(float(invoice.tax_amount), 240.00)

        # Verificar que el ítem existente se actualizó correctamente
        item1 = invoice.items.get(service=self.service_obj)
        self.assertEqual(item1.quantity, 2)
        self.assertEqual(item1.description, 'Licencia de software actualizada')

        # Verificar que el nuevo ítem se añadió correctamente
        item2 = invoice.items.get(service=self.service_obj_2)
        self.assertEqual(item2.quantity, 1)
        self.assertEqual(item2.description, 'Soporte Adicional')

    def test_update_invoice_remove_items(self):
        """
        Verifica que se pueden eliminar ítems al actualizar una factura.
        """
        # Crear una factura inicial con 2 ítems
        response = self.client.post(self.invoice_list_url, self.valid_invoice_data, format='json')
        # Asegúrate de que la creación inicial fue exitosa antes de continuar
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        invoice = Invoice.objects.get(pk=response.data['id'])
        self.assertEqual(invoice.items.count(), 2)

        # Datos para actualizar: eliminar todos los ítems (enviar lista vacía)
        updated_invoice_data = {
            'client': self.client_obj.pk,
            'issue_date': str(date.today()),
            'due_date': str(date.today() + timedelta(days=30)),
            'status': 'draft',
            'notes': 'Factura sin ítems.', # Añadir notas
            'items': [] # Lista de ítems vacía
        }

        response = self.client.put(self.invoice_detail_url(invoice.pk), updated_invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK) # <-- ¡CORRECCIÓN AQUÍ! Esperar 200 OK
        invoice.refresh_from_db()
        self.assertEqual(invoice.items.count(), 0) # No debe haber ítems
        self.assertAlmostEqual(float(invoice.total_amount), 0.00) # Total debe ser 0
        self.assertAlmostEqual(float(invoice.tax_amount), 0.00) # IVA debe ser 0

    def test_update_invoice_item_invalid_data_fails(self):
        """
        Verifica que la actualización falla si los ítems anidados tienen datos inválidos.
        """
        # Crear una factura inicial
        response = self.client.post(self.invoice_list_url, self.valid_invoice_data, format='json')
        # Asegúrate de que la creación inicial fue exitosa antes de continuar
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        invoice = Invoice.objects.get(pk=response.data['id'])

        # Datos para actualizar con un ítem inválido (cantidad 0)
        invalid_items_data = [
            {
                'service': self.service_obj.pk,
                'description': 'Licencia',
                'quantity': 0, # Cantidad inválida
                'price': '500.00',
                'tax_percentage': '21.00'
            }
        ]
        updated_invoice_data = {
            'client': self.client_obj.pk,
            'issue_date': str(date.today()),
            'due_date': str(date.today() + timedelta(days=30)),
            'status': 'pending',
            'notes': 'Intento de actualización con ítem inválido.', # Añadir notas
            'items': invalid_items_data
        }

        response = self.client.put(self.invoice_detail_url(invoice.pk), updated_invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) # Esperamos 400 Bad Request
        self.assertIn('items', response.data)
        self.assertIn('quantity', response.data['items'][0])
        self.assertIn('La cantidad debe ser al menos 1.', response.data['items'][0]['quantity'])
        # Asegúrate de que la factura y sus ítems originales no se modificaron
        invoice.refresh_from_db()
        self.assertEqual(invoice.items.count(), 2) # Sigue teniendo los 2 ítems originales

    # --- Tests adicionales para endpoints específicos de InvoiceItem si los usas directamente ---
    # Si tus vistas InvoiceItemCreate y InvoiceItemRetrieveUpdateDestroy
    # permiten operaciones directas sobre ítems sin pasar por la factura principal,
    # puedes descomentar y usar estos tests.

    # class InvoiceItemDirectTests(APITestCase):
    #     def setUp(self):
    #         self.user = User.objects.create_user(username='testadmin_item_direct', password='TestPassword123')
    #         self.client.force_authenticate(user=self.user)
    #         self.client_obj = Client.objects.create(
    #             name='Cliente Directo', tax_id='B11111111', address='Dir', postal_code='00000',
    #             city='Ciudad', province='Prov', country='País', email='a@b.com', phone='123'
    #         )
    #         self.service_category = ServiceCategory.objects.create(name='CatDirecta')
    #         self.service_obj = Service.objects.create(
    #             name='Servicio Directo', code='DIR001', category=self.service_category, price='100.00'
    #         )
    #         self.invoice = Invoice.objects.create(
    #             client=self.client_obj, issue_date=date.today(), due_date=date.today() + timedelta(days=30), status='draft'
    #         )
    #         self.invoice_item_create_url = reverse('invoice-item-create', kwargs={'invoice_id': self.invoice.pk})
    #         # Nota: para invoice-item-detail, el PK es el del InvoiceItem, no el de la Invoice
    #         # self.invoice_item_detail_url = lambda pk: reverse('invoice-item-detail', kwargs={'invoice_id': self.invoice.pk, 'pk': pk})

    #     def test_create_single_invoice_item_direct(self):
    #         """
    #         Verifica que se puede crear un solo ítem de factura directamente
    #         asociado a una factura existente.
    #         """
    #         data = {
    #             'service': self.service_obj.pk,
    #             'description': 'Nuevo ítem directo',
    #             'quantity': 3,
    #             'price': '100.00',
    #             'tax_percentage': '21.00'
    #         }
    #         response = self.client.post(self.invoice_item_create_url, data, format='json')
    #         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #         self.assertEqual(self.invoice.items.count(), 1)
    #         self.invoice.refresh_from_db()
    #         self.invoice.calculate_total() # Recalcular el total después de añadir el ítem
    #         self.assertAlmostEqual(float(self.invoice.total_amount), 300.00) # 3 * 100
    #         self.assertAlmostEqual(float(self.invoice.tax_amount), 63.00) # 300 * 0.21

    # class InvoiceStatusUpdateTests(APITestCase):
    #     def setUp(self):
    #         self.user = User.objects.create_user(username='testadmin_status', password='TestPassword123')
    #         self.client.force_authenticate(user=self.user)
    #         self.client_obj = Client.objects.create(
    #             name='Cliente Estado', tax_id='B22222222', address='Dir', postal_code='00000',
    #             city='Ciudad', province='Prov', country='País', email='c@d.com', phone='456'
    #         )
    #         self.invoice = Invoice.objects.create(
    #             client=self.client_obj, issue_date=date.today(), due_date=date.today() + timedelta(days=30), status='draft'
    #         )
    #         self.invoice_status_update_url = reverse('invoice-status-update', kwargs={'pk': self.invoice.pk})

    #     def test_update_invoice_status_success(self):
    #         """
    #         Verifica que se puede actualizar el estado de una factura.
    #         """
    #         data = {'status': 'paid'}
    #         response = self.client.patch(self.invoice_status_update_url, data, format='json')
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.invoice.refresh_from_db()
    #         self.assertEqual(self.invoice.status, 'paid')

    #     def test_update_invoice_status_invalid_value(self):
    #         """
    #         Verifica que la actualización de estado falla con un valor inválido.
    #         """
    #         data = {'status': 'estado_invalido'}
    #         response = self.client.patch(self.invoice_status_update_url, data, format='json')
    #         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #         self.assertIn('status', response.data)
    #         self.assertIn('El estado proporcionado no es válido.', response.data['status'])

