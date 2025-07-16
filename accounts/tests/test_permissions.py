from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group, Permission
from clients.models import Client

class PermissionTest(APITestCase):
    def setUp(self):
        """Crea usuarios con diferentes roles y datos de prueba."""
        # Crear grupos de roles
        self.admin_group, _ = Group.objects.get_or_create(name='admin')
        self.staff_group, _ = Group.objects.get_or_create(name='staff')
        self.client_group, _ = Group.objects.get_or_create(name='client')
        
        # Crear usuarios para cada rol
        self.admin_user = User.objects.create_user('adminuser', 'pass', is_staff=True, is_superuser=True)
        self.admin_user.groups.add(self.admin_group)
        
        self.staff_user = User.objects.create_user('staffuser', 'pass', is_staff=True)
        self.staff_user.groups.add(self.staff_group)
        
        self.client_user = User.objects.create_user('clientuser', 'pass')
        self.client_user.groups.add(self.client_group)

        # Crear un recurso para probar el acceso
        self.client_resource = Client.objects.create(name='Cliente de Permisos', email='perm@test.com')
        self.client_list_url = reverse('client-list') # URL del CRUD de clientes

    def test_admin_can_access_everything(self):
        """Test para verificar que un admin puede listar todos los clientes."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.client_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_staff_can_access_clients(self):
        """Test para verificar que el personal (staff) puede listar clientes."""
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.get(self.client_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_client_user_cannot_list_clients(self):
        """Test para verificar que un usuario con rol 'client' no puede listar todos los clientes."""
        # Asumiendo que los clientes solo pueden ver su propia información, no la lista completa.
        self.client.force_authenticate(user=self.client_user)
        response = self.client.get(self.client_list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)