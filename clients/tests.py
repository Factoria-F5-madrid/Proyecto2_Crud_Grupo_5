# Proyecto2__Crud_Grupo_5/clients/tests.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Client

User = get_user_model()

class ClientTests(APITestCase):
    """
    Clase de tests para el modelo Client.
    Verifica operaciones CRUD y validaciones.
    """

    def setUp(self):
        # Crear un usuario para autenticar las peticiones
        self.user = User.objects.create_user(username='testadmin', password='TestPassword123')
        # Autenticar el cliente de test
        self.client.force_authenticate(user=self.user)

        # URL para la lista de clientes (POST para crear, GET para listar)
        self.client_list_url = reverse('client-list-create')
        # URL para un cliente específico (GET, PUT, PATCH, DELETE por ID)
        self.client_detail_url = lambda pk: reverse('client-detail', kwargs={'pk': pk})

        # Datos base para un cliente válido
        self.valid_client_data = {
            'name': 'Empresa Test S.L.',
            'tax_id': 'B12345678',
            'address': 'Calle Falsa 123',
            'postal_code': '28001',
            'city': 'Madrid',
            'province': 'Madrid',
            'country': 'España',
            'email': 'contacto@empresatest.com',
            'phone': '912345678',
            'contact_person': 'Juan Pérez',
            'is_active': True,
            'notes': 'Notas de prueba.'
        }

    # --- Tests de Creación (POST) ---

    def test_create_client_success(self):
        """
        Verifica que se puede crear un cliente exitosamente con datos válidos.
        """
        response = self.client.post(self.client_list_url, self.valid_client_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 1)
        self.assertEqual(Client.objects.get().name, 'Empresa Test S.L.')

    def test_create_client_no_name(self):
        """
        Verifica que la creación falla si no se proporciona el nombre.
        """
        data = self.valid_client_data.copy()
        data.pop('name')
        response = self.client.post(self.client_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('El nombre del cliente es obligatorio.', response.data['name'])

    def test_create_client_blank_name(self):
        """
        Verifica que la creación falla si el nombre está en blanco.
        """
        data = self.valid_client_data.copy()
        data['name'] = ''
        response = self.client.post(self.client_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('El nombre del cliente no puede estar en blanco.', response.data['name'])

    def test_create_client_duplicate_tax_id(self):
        """
        Verifica que la creación falla si el NIF/CIF ya existe.
        """
        # Crea un cliente existente con el mismo tax_id
        Client.objects.create(**self.valid_client_data)
        data = self.valid_client_data.copy()
        data['name'] = 'Otra Empresa' # Cambia el nombre para evitar conflicto
        response = self.client.post(self.client_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('tax_id', response.data)
        self.assertIn('Ya existe un cliente con este NIF/CIF. Debe ser único.', response.data['tax_id'])

    def test_create_client_invalid_email(self):
        """
        Verifica que la creación falla si el formato del email es inválido.
        """
        data = self.valid_client_data.copy()
        data['email'] = 'invalid-email'
        response = self.client.post(self.client_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn('Por favor, introduce un formato de correo electrónico válido.', response.data['email'])

    def test_create_client_no_address(self):
        """
        Verifica que la creación falla si no se proporciona la dirección.
        """
        data = self.valid_client_data.copy()
        data.pop('address')
        response = self.client.post(self.client_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('address', response.data)
        self.assertIn('La dirección es obligatoria.', response.data['address'])

    # --- Tests de Actualización (PUT/PATCH) ---

    def test_update_client_success(self):
        """
        Verifica que se puede actualizar un cliente exitosamente.
        """
        client = Client.objects.create(**self.valid_client_data)
        updated_data = self.valid_client_data.copy()
        updated_data['name'] = 'Empresa Actualizada S.A.'
        updated_data['email'] = 'nuevo@empresatest.com' # Cambia también el email

        response = self.client.put(self.client_detail_url(client.pk), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        client.refresh_from_db() # Recarga el objeto desde la DB para ver los cambios
        self.assertEqual(client.name, 'Empresa Actualizada S.A.')
        self.assertEqual(client.email, 'nuevo@empresatest.com')

    def test_update_client_duplicate_tax_id_fails(self):
        """
        Verifica que la actualización falla si se intenta usar un NIF/CIF ya existente en otro cliente.
        """
        client1 = Client.objects.create(**self.valid_client_data)
        # ¡CORRECCIÓN AQUÍ! Definir client2 correctamente
        client2_data = self.valid_client_data.copy()
        client2_data['tax_id'] = 'A98765432' # NIF/CIF diferente
        client2_data['name'] = 'Otra Empresa'
        client2_data['email'] = 'otra@empresa.com' # Email diferente
        client2_data['phone'] = '999888777' # Teléfono diferente
        client2 = Client.objects.create(**client2_data)

        # Intentar actualizar client1 con el tax_id de client2
        update_data = self.valid_client_data.copy()
        update_data['tax_id'] = client2.tax_id # Usar el tax_id del otro cliente
        response = self.client.put(self.client_detail_url(client1.pk), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('tax_id', response.data)
        self.assertIn('Ya existe un cliente con este NIF/CIF. Debe ser único.', response.data['tax_id'])

    def test_partial_update_client_success(self):
        """
        Verifica que se puede realizar una actualización parcial de un cliente.
        """
        client = Client.objects.create(**self.valid_client_data)
        partial_data = {
            'phone': '987654321',
            'contact_person': 'María García'
        }
        response = self.client.patch(self.client_detail_url(client.pk), partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        client.refresh_from_db()
        self.assertEqual(client.phone, '987654321')
        self.assertEqual(client.contact_person, 'María García')
        # Verifica que otros campos no cambiaron
        self.assertEqual(client.name, self.valid_client_data['name'])

