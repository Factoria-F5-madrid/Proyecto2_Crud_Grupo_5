from django.test import TestCase, Client as TestClient
from django.urls import reverse
from clients.models import Client
from django.contrib.auth.models import User

class ClientViewTest(TestCase):
    def setUp(self):
        """Configuración inicial para tests de vistas"""
        # Crear usuario para autenticación
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Cliente de prueba para Django (no confundir con el modelo Client)
        self.test_client = TestClient()
        
        # Crear datos de prueba
        self.client_data = {
            'name': 'Cliente Vista',
            'email': 'vista@cliente.com',
            'phone': '911223344',
            'address': 'Dirección de prueba'
        }
        self.test_model_client = Client.objects.create(**self.client_data)
        
        # URLs
        self.list_url = reverse('client-list-create')
        self.detail_url = reverse('client-detail-view', args=[self.test_model_client.id])
        self.create_url = reverse('client-create-view')
        self.update_url = reverse('client-update-view', args=[self.test_model_client.id])
        self.delete_url = reverse('client-delete-view', args=[self.test_model_client.id])
    
    def test_client_list_view(self):
        """Test para verificar vista de listado de clientes"""
        self.test_client.login(username='testuser', password='testpass123')
        response = self.test_client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cliente Vista')
        self.assertContains(response, 'vista@cliente.com')
    
    def test_client_detail_view(self):
        """Test para verificar vista de detalle de cliente"""
        self.test_client.login(username='testuser', password='testpass123')
        response = self.test_client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Cliente Vista')
        self.assertContains(response, 'vista@cliente.com')
    
    def test_client_create_view(self):
        """Test para verificar vista de creación de cliente"""
        self.test_client.login(username='testuser', password='testpass123')
        response = self.test_client.post(self.create_url, {
            'name': 'Nuevo Cliente Vista',
            'email': 'nuevo@vista.com',
            'phone': '922334455',
            'address': 'Nueva dirección vista'
        })
        self.assertEqual(response.status_code, 302)  # Redirección después de crear
        self.assertTrue(Client.objects.filter(email='nuevo@vista.com').exists())
    
    def test_client_update_view(self):
        """Test para verificar vista de actualización de cliente"""
        self.test_client.login(username='testuser', password='testpass123')
        response = self.test_client.post(self.update_url, {
            'name': 'Cliente Vista Actualizado',
            'email': 'vista@cliente.com',
            'phone': '911223344',
            'address': 'Dirección vista actualizada'
        })
        self.assertEqual(response.status_code, 302)  # Redirección después de actualizar
        self.test_model_client.refresh_from_db()
        self.assertEqual(self.test_model_client.name, 'Cliente Vista Actualizado')
        self.assertEqual(self.test_model_client.address, 'Dirección vista actualizada')
    
    def test_client_delete_view(self):
        """Test para verificar vista de eliminación de cliente"""
        self.test_client.login(username='testuser', password='testpass123')
        response = self.test_client.post(self.delete_url)
        self.assertEqual(response.status_code, 302)  # Redirección después de eliminar
        self.assertFalse(Client.objects.filter(id=self.test_model_client.id).exists())