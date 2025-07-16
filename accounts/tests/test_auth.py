from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class AuthenticationTest(APITestCase):
    def setUp(self):
        """Crea un usuario para las pruebas de autenticación."""
        self.username = 'authuser'
        self.password = 'authpass123'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        
        # URL para obtener el token JWT (depende de la librería, p.ej. djangorestframework-simplejwt)
        self.login_url = reverse('token_obtain_pair') # Ajusta este nombre de URL

    def test_successful_login(self):
        """Test para un login exitoso que devuelve tokens."""
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_failed_login_wrong_password(self):
        """Test para un login fallido con contraseña incorrecta."""
        data = {'username': self.username, 'password': 'wrongpassword'}
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse('access' in response.data)

    def test_failed_login_nonexistent_user(self):
        """Test para un login fallido con un usuario que no existe."""
        data = {'username': 'nouser', 'password': 'somepassword'}
        response = self.client.post(self.login_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)