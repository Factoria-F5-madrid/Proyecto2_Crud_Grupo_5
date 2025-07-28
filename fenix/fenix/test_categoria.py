import tempfile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from PIL import Image
import os
from io import BytesIO

# Importar modelos y serializadores para que los tests funcionen.
# En un proyecto real, estos estarían definidos en tu `models.py` y `serializers.py`
# Aquí los creamos de forma simplificada para el propósito del test.
# ASUNCION: Tienes un modelo Category con al menos un campo 'name' y 'description'.
# ASUNCION: Tienes un modelo Product con al menos un campo 'name' y una FK 'category'.

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        # Asegúrate de que el nombre de la tabla sea 'categoria_category' si tu app se llama 'categoría'
        # o ajusta el app_label si usas un nombre diferente en settings.py
        app_label = 'categoria' 
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    # Otros campos de Product si son relevantes para los tests de CategoryDetailSerializer
    
    class Meta:
        app_label = 'prenda' # Asume que Product está en la app 'prenda'

    def __str__(self):
        return self.name

# Aunque no nos has proporcionado los serializadores, los inferimos
# y definimos aquí mínimamente para que los tests puedan ejecutarse.
from rest_framework import serializers

class ProductInDetailCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class CategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductInDetailCategorySerializer(many=True, read_only=True) # Anidar productos
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products']

# Fin de la sección de modelos/serializadores inferidos


class CategoryAPITests(APITestCase):
    """
    Clase de tests para las vistas de la API de Categorías.
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Configura datos de prueba que se ejecutarán una vez para toda la clase de test.
        """
        cls.category1 = Category.objects.create(name='Ropa Deportiva', description='Categoría para indumentaria deportiva.')
        cls.category2 = Category.objects.create(name='Calzado', description='Categoría para todo tipo de calzado.')
        cls.category3 = Category.objects.create(name='Accesorios', description='Accesorios de moda.')

        # Crear productos asociados para probar CategoryDetailSerializer
        Product.objects.create(name='Zapatillas Running', category=cls.category1, price=80.00, stock=50)
        Product.objects.create(name='Leggings Deportivos', category=cls.category1, price=35.00, stock=100)
        Product.objects.create(name='Botas de Cuero', category=cls.category2, price=120.00, stock=20)


    def test_list_categories(self):
        """
        Verifica que la vista GET /api/categorias/ lista todas las categorías.
        """
        # 1. Definir la URL para la vista de listado/creación de categorías.
        # Usamos 'categoría_api:category-list-create' basándonos en tu fenix/urls.py
        url = reverse('categoría_api:category-list-create')
        
        # 2. Realizar la petición GET.
        response = self.client.get(url)
        
        # 3. Verificar el código de estado HTTP.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 4. Verificar que la cantidad de categorías devueltas es la correcta.
        self.assertEqual(len(response.data), 3) # Tenemos 3 categorías de prueba
        
        # 5. Opcional: Verificar que los datos de una categoría son correctos.
        # Serializamos los objetos para comparar con la respuesta de la API.
        expected_data = CategorySerializer(self.category1).data
        # Aseguramos que la categoría 1 esté en la respuesta (el orden puede variar por el ordenamiento por defecto)
        self.assertIn(expected_data, response.data)

    def test_create_category_success(self):
        """
        Verifica la creación exitosa de una nueva categoría via POST.
        """
        url = reverse('categoría_api:category-list-create')
        new_category_data = {'name': 'Electrónica', 'description': 'Gadgets y dispositivos electrónicos.'}
        
        # Realizar la petición POST.
        response = self.client.post(url, new_category_data, format='json')
        
        # Verificar el código de estado 201 Created.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que la categoría fue creada en la base de datos.
        self.assertTrue(Category.objects.filter(name='Electrónica').exists())
        
        # Verificar que los datos en la respuesta coinciden con los enviados (incluyendo el ID generado).
        self.assertEqual(response.data['name'], 'Electrónica')
        self.assertEqual(response.data['description'], 'Gadgets y dispositivos electrónicos.')

    def test_create_category_duplicate_name(self):
        """
        Verifica que no se puede crear una categoría con un nombre duplicado.
        """
        url = reverse('categoría_api:category-list-create')
        # Intentar crear una categoría con un nombre que ya existe (Ropa Deportiva).
        duplicate_category_data = {'name': 'Ropa Deportiva', 'description': 'Descripción de prueba.'}
        
        response = self.client.post(url, duplicate_category_data, format='json')
        
        # Verificar el código de estado 409 Conflict.
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn('Category with this name already exists.', response.data['detail'])

    def test_create_category_invalid_data(self):
        """
        Verifica que la creación falla con datos inválidos (ej. campo requerido faltante).
        """
        url = reverse('categoría_api:category-list-create')
        # Datos inválidos: falta el campo 'name'.
        invalid_data = {'description': 'Categoría sin nombre.'}
        
        response = self.client.post(url, invalid_data, format='json')
        
        # Verificar el código de estado 400 Bad Request.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data) # Asegurar que el error es sobre el campo 'name'.

    def test_retrieve_category_detail_success(self):
        """
        Verifica que se puede obtener el detalle de una categoría existente, incluyendo productos.
        """
        # Usamos el ID de category1 creado en setUpTestData.
        url = reverse('categoría_api:category-detail', kwargs={'pk': self.category1.pk})
        
        response = self.client.get(url)
        
        # Verificar el código de estado 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que los datos de la categoría son correctos.
        self.assertEqual(response.data['name'], self.category1.name)
        self.assertEqual(response.data['description'], self.category1.description)
        
        # Verificar que se incluyen los productos anidados (gracias a CategoryDetailSerializer).
        self.assertIn('products', response.data)
        self.assertIsInstance(response.data['products'], list)
        self.assertTrue(len(response.data['products']) > 0)
        # Opcional: verificar un producto específico anidado
        product_names_in_response = [p['name'] for p in response.data['products']]
        self.assertIn('Zapatillas Running', product_names_in_response)
        self.assertIn('Leggings Deportivos', product_names_in_response)


    def test_retrieve_category_not_found(self):
        """
        Verifica que se obtiene un 404 si la categoría no existe.
        """
        non_existent_id = 999
        url = reverse('categoría_api:category-detail', kwargs={'pk': non_existent_id})
        
        response = self.client.get(url)
        
        # Verificar el código de estado 404 Not Found.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Category not found.', response.data['detail'])

    def test_update_category_put_success(self):
        """
        Verifica la actualización completa (PUT) exitosa de una categoría.
        """
        url = reverse('categoría_api:category-detail', kwargs={'pk': self.category1.pk})
        updated_data = {'name': 'Ropa de Gimnasio', 'description': 'Nueva descripción para ropa deportiva.'}
        
        response = self.client.put(url, updated_data, format='json')
        
        # Verificar el código de estado 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que la categoría fue actualizada en la base de datos.
        self.category1.refresh_from_db() # Recargar la instancia desde la DB
        self.assertEqual(self.category1.name, 'Ropa de Gimnasio')
        self.assertEqual(self.category1.description, 'Nueva descripción para ropa deportiva.')
        
        # Verificar que la respuesta contiene los datos actualizados.
        self.assertEqual(response.data['name'], 'Ropa de Gimnasio')

    def test_update_category_put_duplicate_name(self):
        """
        Verifica que la actualización (PUT) falla si el nuevo nombre ya existe en otra categoría.
        """
        url = reverse('categoría_api:category-detail', kwargs={'pk': self.category1.pk})
        # Intentar cambiar el nombre de category1 al nombre de category2.
        updated_data = {'name': self.category2.name, 'description': 'Test description.'}
        
        response = self.client.put(url, updated_data, format='json')
        
        # Verificar el código de estado 409 Conflict.
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn('Category with this name already exists.', response.data['detail'])

    def test_update_category_put_invalid_data(self):
        """
        Verifica que la actualización completa (PUT) falla con datos inválidos.
        """
        url = reverse('categoría_api:category-detail', kwargs={'pk': self.category1.pk})
        # Datos inválidos: campo 'name' vacío (asumiendo que es requerido y no puede ser vacío).
        invalid_data = {'name': '', 'description': 'Invalid update.'}
        
        response = self.client.put(url, invalid_data, format='json')
        
        # Verificar el código de estado 400 Bad Request.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_update_category_patch_success(self):
        """
        Verifica la actualización parcial (PATCH) exitosa de una categoría.
        """
        url = reverse('categoría_api:category-detail', kwargs={'pk': self.category1.pk})
        # Solo actualizamos la descripción.
        partial_data = {'description': 'Descripción actualizada parcialmente.'}
        
        response = self.client.patch(url, partial_data, format='json')
        
        # Verificar el código de estado 200 OK.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que solo la descripción fue actualizada en la base de datos.
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.description, 'Descripción actualizada parcialmente.')
        self.assertEqual(self.category1.name, 'Ropa Deportiva') # El nombre debe permanecer igual.

    def test_update_category_patch_duplicate_name(self):
        """
        Verifica que la actualización parcial (PATCH) falla si el nuevo nombre ya existe.
        """
        url = reverse('categoría_api:category-detail', kwargs={'pk': self.category1.pk})
        # Intentar cambiar el nombre de category1 al nombre de category2 usando PATCH.
        partial_data = {'name': self.category2.name}
        
        response = self.client.patch(url, partial_data, format='json')
        
        # Verificar el código de estado 409 Conflict.
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn('Category with this name already exists.', response.data['detail'])

    def test_delete_category_success(self):
        """
        Verifica la eliminación exitosa de una categoría.
        """
        # Usamos category3 para eliminarla, así no afectamos las que tienen productos asociados.
        url = reverse('categoría_api:category-detail', kwargs={'pk': self.category3.pk})
        
        response = self.client.delete(url)
        
        # Verificar el código de estado 204 No Content.
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verificar que la categoría ya no existe en la base de datos.
        self.assertFalse(Category.objects.filter(pk=self.category3.pk).exists())
        
        # Verificar que la eliminación de category3 no afectó a category1 o category2.
        self.assertTrue(Category.objects.filter(pk=self.category1.pk).exists())
        self.assertTrue(Category.objects.filter(pk=self.category2.pk).exists())


    def test_delete_category_not_found(self):
        """
        Verifica que se obtiene un 404 al intentar eliminar una categoría no existente.
        """
        non_existent_id = 999
        url = reverse('categoría_api:category-detail', kwargs={'pk': non_existent_id})
        
        response = self.client.delete(url)
        
        # Verificar el código de estado 404 Not Found.
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('Category not found.', response.data['detail'])

    def test_list_categories_search_filter(self):
        """
        Verifica que el filtro de búsqueda por nombre funciona correctamente.
        """
        url = reverse('categoría_api:category-list-create')
        # Buscar por 'deportiva' que está en 'Ropa Deportiva'
        response = self.client.get(f'{url}?search=Deportiva')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Ropa Deportiva')

    def test_list_categories_ordering_filter(self):
        """
        Verifica que el ordenamiento por nombre funciona correctamente.
        """
        url = reverse('categoría_api:category-list-create')
        # Ordenar por nombre ascendente
        response = self.client.get(f'{url}?ordering=name')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        # Accesorios, Calzado, Ropa Deportiva (orden alfabético)
        self.assertEqual(response.data[0]['name'], 'Accesorios')
        self.assertEqual(response.data[1]['name'], 'Calzado')
        self.assertEqual(response.data[2]['name'], 'Ropa Deportiva')

    def test_list_categories_no_filter(self):
        """
        Verifica que el listado sin filtros ni búsqueda retorna todas las categorías.
        """
        url = reverse('categoría_api:category-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3) # Todas las categorías creadas en setUpTestData.