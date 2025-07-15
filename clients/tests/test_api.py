from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from clients.models import Client
from django.contrib.auth.models import User

class ClientAPITest(APITestCase):
    def setUp(self):
        """Configuración inicial para los tests de API"""
        # Crear usuario para autenticación
        self.username = 'testuser'
        self.password = 'testpass123'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )
        
        # Datos de prueba
        self.client_data = {
            'name': 'Cliente API',
            'email': 'api@cliente.com',
            'phone': '900123456',
            'address': 'Dirección de prueba'
        }
        
        # Crear cliente de prueba
        self.test_client = Client.objects.create(**self.client_data)
        
        # URLs
        self.list_url = reverse('client-list')
        self.detail_url = reverse('client-detail', args=[self.test_client.id])
    
    def authenticate(self):
        """Autenticar usuario para los tests"""
        self.client.login(username=self.username, password=self.password)
    
    def test_get_client_list(self):
        """Test para obtener lista de clientes"""
        self.authenticate()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_client_detail(self):
        """Test para obtener detalle de un cliente"""
        self.authenticate()
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Cliente API')
        self.assertEqual(response.data['email'], 'api@cliente.com')
    
    def test_create_client(self):
        """Test para crear un nuevo cliente"""
        self.authenticate()
        new_client_data = {
            'name': 'Nuevo Cliente',
            'email': 'nuevo@cliente.com',
            'phone': '911223344',
            'address': 'Nueva dirección'
        }
        response = self.client.post(self.list_url, new_client_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Client.objects.count(), 2)
        self.assertEqual(Client.objects.get(email='nuevo@cliente.com').name, 'Nuevo Cliente')
    
    def test_update_client(self):
        """Test para actualizar un cliente existente"""
        self.authenticate()
        updated_data = {
            'name': 'Cliente Actualizado',
            'email': 'api@cliente.com',
            'phone': '900123456',
            'address': 'Dirección actualizada'
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_client.refresh_from_db()
        self.assertEqual(self.test_client.name, 'Cliente Actualizado')
        self.assertEqual(self.test_client.address, 'Dirección actualizada')
    
    def test_delete_client(self):
        """Test para eliminar un cliente"""
        self.authenticate()
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Client.objects.count(), 0)