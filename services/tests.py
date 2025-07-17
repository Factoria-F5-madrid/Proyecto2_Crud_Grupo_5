# Proyecto2__Crud_Grupo_5/services/tests.py

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import ServiceCategory, Service

User = get_user_model()

class ServiceCategoryTests(APITestCase):
    """
    Clase de tests para el modelo ServiceCategory.
    Verifica operaciones CRUD y validaciones.
    """

    def setUp(self):
        # Crear un usuario para autenticar las peticiones
        self.user = User.objects.create_user(username='testadmin', password='TestPassword123')
        # Autenticar el cliente de test
        self.client.force_authenticate(user=self.user)

        # URL para la lista de categorías (POST para crear, GET para listar)
        self.category_list_url = reverse('category-list-create')
        # URL para una categoría específica (GET, PUT, PATCH, DELETE por ID)
        self.category_detail_url = lambda pk: reverse('category-detail', kwargs={'pk': pk})

        self.valid_category_data = {
            'name': 'Consultoría',
            'description': 'Servicios de consultoría empresarial.',
            'is_active': True
        }

    # --- Tests de Creación (POST) ---

    def test_create_service_category_success(self):
        """
        Verifica que se puede crear una categoría de servicio exitosamente.
        """
        response = self.client.post(self.category_list_url, self.valid_category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ServiceCategory.objects.count(), 1)
        self.assertEqual(ServiceCategory.objects.get().name, 'Consultoría')

    def test_create_service_category_no_name(self):
        """
        Verifica que la creación falla si no se proporciona el nombre.
        """
        data = self.valid_category_data.copy()
        data.pop('name')
        response = self.client.post(self.category_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('El nombre de la categoría es obligatorio.', response.data['name'])

    def test_create_service_category_blank_name(self):
        """
        Verifica que la creación falla si el nombre está en blanco.
        """
        data = self.valid_category_data.copy()
        data['name'] = ''
        response = self.client.post(self.category_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('El nombre de la categoría no puede estar en blanco.', response.data['name'])

    def test_create_service_category_duplicate_name(self):
        """
        Verifica que la creación falla si el nombre de la categoría ya existe.
        """
        ServiceCategory.objects.create(**self.valid_category_data)
        response = self.client.post(self.category_list_url, self.valid_category_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('Ya existe una categoría de servicio con este nombre. Debe ser único.', response.data['name'])

    # --- Tests de Actualización (PUT/PATCH) ---

    def test_update_service_category_success(self):
        """
        Verifica que se puede actualizar una categoría de servicio exitosamente.
        """
        category = ServiceCategory.objects.create(**self.valid_category_data)
        updated_data = self.valid_category_data.copy()
        updated_data['name'] = 'Consultoría Avanzada'
        response = self.client.put(self.category_detail_url(category.pk), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, 'Consultoría Avanzada')

    def test_update_service_category_duplicate_name_fails(self):
        """
        Verifica que la actualización falla si se intenta usar un nombre de categoría ya existente.
        """
        category1 = ServiceCategory.objects.create(name='Cat1', description='Desc1')
        category2 = ServiceCategory.objects.create(name='Cat2', description='Desc2')
        update_data = {'name': 'Cat2'} # Intentar cambiar Cat1 a Cat2
        response = self.client.put(self.category_detail_url(category1.pk), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('Ya existe una categoría de servicio con este nombre. Debe ser único.', response.data['name'])


class ServiceTests(APITestCase):
    """
    Clase de tests para el modelo Service.
    Verifica operaciones CRUD y validaciones.
    """

    def setUp(self):
        # Crear un usuario para autenticar las peticiones
        self.user = User.objects.create_user(username='testadmin', password='TestPassword123')
        # Autenticar el cliente de test
        self.client.force_authenticate(user=self.user)

        # URL para la lista de servicios (POST para crear, GET para listar)
        self.service_list_url = reverse('service-list-create')
        # URL para un servicio específico (GET, PUT, PATCH, DELETE por ID)
        self.service_detail_url = lambda pk: reverse('service-detail', kwargs={'pk': pk})

        # Crear una categoría de servicio para usar en los tests de Service
        self.category = ServiceCategory.objects.create(name='Desarrollo', description='Servicios de desarrollo de software')

        # Datos base para un servicio válido (usando la instancia de categoría)
        self.valid_service_data = {
            'name': 'Desarrollo Web',
            'code': 'WEBDEV001',
            'description': 'Servicio de desarrollo de sitios web.',
            'category': self.category, # <-- ¡Pasa la instancia completa para creación directa de modelo!
            'price': '1500.00',
            'tax_percentage': '21.00',
            'is_active': True
        }

    # --- Tests de Creación (POST) ---

    def test_create_service_success(self):
        """
        Verifica que se puede crear un servicio exitosamente con datos válidos.
        """
        # Para el POST a la API, el serializer espera el PK de la categoría
        data_for_post = self.valid_service_data.copy()
        data_for_post['category'] = self.category.pk 

        response = self.client.post(self.service_list_url, data_for_post, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Service.objects.count(), 1)
        self.assertEqual(Service.objects.get().name, 'Desarrollo Web')

    def test_create_service_no_name(self):
        """
        Verifica que la creación falla si no se proporciona el nombre.
        """
        data = self.valid_service_data.copy()
        data.pop('name')
        data['category'] = self.category.pk # Para el POST, usamos el PK
        response = self.client.post(self.service_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)
        self.assertIn('El nombre del servicio es obligatorio.', response.data['name'])

    def test_create_service_duplicate_code(self):
        """
        Verifica que la creación falla si el código de servicio ya existe.
        """
        # Crea el primer servicio usando la instancia de categoría (self.valid_service_data ya la tiene)
        Service.objects.create(**self.valid_service_data) # <-- Aquí se usa la instancia de categoría

        data = self.valid_service_data.copy()
        data['name'] = 'Otro Servicio' # Cambiar nombre para evitar conflicto
        data['category'] = self.category.pk # Para el POST, usamos el PK
        response = self.client.post(self.service_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('code', response.data)
        self.assertIn('Ya existe un servicio con este código. Debe ser único.', response.data['code'])

    def test_create_service_no_category(self):
        """
        Verifica que la creación falla si no se proporciona la categoría.
        """
        data = self.valid_service_data.copy()
        data.pop('category') # Eliminar la categoría
        response = self.client.post(self.service_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('category', response.data)
        self.assertIn('La categoría del servicio es obligatoria.', response.data['category'])

    def test_create_service_non_existent_category(self):
        """
        Verifica que la creación falla si la categoría no existe.
        """
        data = self.valid_service_data.copy()
        data['category'] = 9999 # ID de categoría que no existe
        response = self.client.post(self.service_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('category', response.data)
        self.assertIn('La categoría de servicio con el ID proporcionado no existe.', response.data['category'])

    def test_create_service_negative_price(self):
        """
        Verifica que la creación falla si el precio es negativo.
        """
        data = self.valid_service_data.copy()
        data['price'] = '-10.00' # Precio negativo
        data['category'] = self.category.pk # Para el POST, usamos el PK
        response = self.client.post(self.service_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)
        self.assertIn('El precio del servicio debe ser mayor que cero.', response.data['price'])

    def test_create_service_zero_price(self):
        """
        Verifica que la creación falla si el precio es cero.
        """
        data = self.valid_service_data.copy()
        data['price'] = '0.00' # Precio cero
        data['category'] = self.category.pk # Para el POST, usamos el PK
        response = self.client.post(self.service_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)
        self.assertIn('El precio del servicio debe ser mayor que cero.', response.data['price'])

    def test_create_service_tax_percentage_out_of_range(self):
        """
        Verifica que la creación falla si el porcentaje de IVA está fuera de rango (ej. > 100).
        """
        data = self.valid_service_data.copy()
        data['tax_percentage'] = '101.00' # Fuera de rango
        data['category'] = self.category.pk # Para el POST, usamos el PK
        response = self.client.post(self.service_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('tax_percentage', response.data)
        self.assertIn('El porcentaje de IVA no puede exceder 100.', response.data['tax_percentage'])

    # --- Tests de Actualización (PUT/PATCH) ---

    def test_update_service_success(self):
        """
        Verifica que se puede actualizar un servicio exitosamente.
        """
        # Crea el servicio inicial usando la instancia de categoría
        service = Service.objects.create(**self.valid_service_data) # <-- ¡CORRECCIÓN AQUÍ!

        updated_data = self.valid_service_data.copy()
        updated_data['name'] = 'Desarrollo Móvil'
        updated_data['price'] = '2000.00'
        updated_data['category'] = self.category.pk # Para el PUT, usamos el PK

        response = self.client.put(self.service_detail_url(service.pk), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        service.refresh_from_db()
        self.assertEqual(service.name, 'Desarrollo Móvil')
        self.assertEqual(str(service.price), '2000.00')

    def test_update_service_duplicate_code_fails(self):
        """
        Verifica que la actualización falla si se intenta usar un código de servicio ya existente.
        """
        # Crea el primer servicio usando la instancia de categoría
        service1 = Service.objects.create(**self.valid_service_data) # <-- ¡CORRECCIÓN AQUÍ!
        
        # Crea el segundo servicio con un código diferente, usando la instancia de categoría
        service2_data_for_create = self.valid_service_data.copy()
        service2_data_for_create['code'] = 'MOBDEV001' # Código diferente
        service2_data_for_create['name'] = 'Servicio Móvil'
        service2_data_for_create['category'] = self.category # Usar la instancia aquí
        service2_data_for_create['price'] = '100.00' # Precio válido
        service2 = Service.objects.create(**service2_data_for_create)

        # Intentar actualizar service1 con el code de service2
        update_data = self.valid_service_data.copy()
        update_data['code'] = service2.code
        update_data['category'] = self.category.pk # Para el PUT, usamos el PK
        response = self.client.put(self.service_detail_url(service1.pk), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('code', response.data)
        self.assertIn('Ya existe un servicio con este código. Debe ser único.', response.data['code'])

