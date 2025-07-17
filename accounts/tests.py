from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

# Obtener el modelo de usuario activo
User = get_user_model()

class RegisterTests(APITestCase):
    """
    Clase de tests para el registro de nuevos usuarios.
    Verifica casos de éxito y fallos de validación.
    """

    def setUp(self):
        # Configuración inicial para cada test
        self.register_url = reverse('register') # URL para el endpoint de registro

    def test_register_success(self):
        """
        Verifica que un usuario se pueda registrar exitosamente con datos válidos.
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Password123',
            'password2': 'Password123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1) # Verifica que se creó un usuario
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_register_no_username(self):
        """
        Verifica que el registro falla si no se proporciona el nombre de usuario.
        """
        data = {
            'email': 'test@example.com',
            'password': 'Password123',
            'password2': 'Password123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('El nombre de usuario es obligatorio.', response.data['username'])

    def test_register_blank_username(self):
        """
        Verifica que el registro falla si el nombre de usuario está en blanco.
        """
        data = {
            'username': '',
            'email': 'test@example.com',
            'password': 'Password123',
            'password2': 'Password123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('El nombre de usuario no puede estar en blanco.', response.data['username'])

    def test_register_duplicate_username(self):
        """
        Verifica que el registro falla si el nombre de usuario ya existe.
        """
        User.objects.create_user(username='existinguser', email='e@example.com', password='Password123')
        data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password': 'Password123',
            'password2': 'Password123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('Este nombre de usuario ya está en uso. Por favor, elige otro.', response.data['username'])

    def test_register_invalid_email(self):
        """
        Verifica que el registro falla si el formato del email es inválido.
        """
        data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'password': 'Password123',
            'password2': 'Password123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn('Por favor, introduce un formato de correo electrónico válido.', response.data['email'])

    def test_register_duplicate_email(self):
        """
        Verifica que el registro falla si el email ya está registrado.
        """
        User.objects.create_user(username='user1', email='duplicate@example.com', password='Password123')
        data = {
            'username': 'user2',
            'email': 'duplicate@example.com',
            'password': 'Password123',
            'password2': 'Password123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)
        self.assertIn('Este correo electrónico ya está registrado. Por favor, inicia sesión o usa otro.', response.data['email'])

    def test_register_password_mismatch(self):
        """
        Verifica que el registro falla si las contraseñas no coinciden.
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Password123',
            'password2': 'Password456'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password2', response.data)
        self.assertIn('Las contraseñas no coinciden.', response.data['password2'])

    def test_register_password_too_short(self):
        """
        Verifica que el registro falla si la contraseña es demasiado corta.
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'Pass1', # Menos de 8 caracteres
            'password2': 'Pass1'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertIn('La contraseña debe tener al menos 8 caracteres.', response.data['password'])

    def test_register_password_no_digit(self):
        """
        Verifica que el registro falla si la contraseña no contiene un número.
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'PasswordABC',
            'password2': 'PasswordABC'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertIn('La contraseña debe contener al menos un número.', response.data['password'])

    def test_register_password_no_uppercase(self):
        """
        Verifica que el registro falla si la contraseña no contiene una letra mayúscula.
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertIn('La contraseña debe contener al menos una letra mayúscula.', response.data['password'])

    def test_register_password_no_lowercase(self):
        """
        Verifica que el registro falla si la contraseña no contiene una letra minúscula.
        """
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'PASSWORD123',
            'password2': 'PASSWORD123'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertIn('La contraseña debe contener al menos una letra minúscula.', response.data['password'])


class ChangePasswordTests(APITestCase):
    """
    Clase de tests para el cambio de contraseña de usuarios.
    Requiere que el usuario esté autenticado.
    """

    def setUp(self):
        # Crear un usuario para autenticar y probar el cambio de contraseña
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='OldPassword123')
        self.change_password_url = reverse('change-password') # URL para el endpoint de cambio de contraseña

        # Autenticar al cliente de test
        self.client.login(username='testuser', password='OldPassword123')

    def test_change_password_success(self):
        """
        Verifica que la contraseña se pueda cambiar exitosamente.
        """
        data = {
            'old_password': 'OldPassword123',
            'new_password': 'NewPassword456'
        }
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Contraseña actualizada correctamente.')

        # Verificar que la nueva contraseña funciona
        self.assertTrue(self.user.check_password('NewPassword456'))

    def test_change_password_unauthenticated(self):
        """
        Verifica que el cambio de contraseña falla si el usuario no está autenticado.
        """
        self.client.logout() # Desautenticar al cliente
        data = {
            'old_password': 'OldPassword123',
            'new_password': 'NewPassword456'
        }
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # No autorizado

    def test_change_password_incorrect_old_password(self):
        """
        Verifica que el cambio de contraseña falla si la contraseña antigua es incorrecta.
        """
        data = {
            'old_password': 'WrongOldPassword',
            'new_password': 'NewPassword456'
        }
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('old_password', response.data)
        self.assertIn('La contraseña actual es incorrecta.', response.data['old_password'])

    def test_change_password_new_password_too_short(self):
        """
        Verifica que el cambio de contraseña falla si la nueva contraseña es demasiado corta.
        """
        data = {
            'old_password': 'OldPassword123',
            'new_password': 'New1' # Menos de 8 caracteres
        }
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password', response.data)
        self.assertIn('La nueva contraseña debe tener al menos 8 caracteres.', response.data['new_password'])

    def test_change_password_new_password_no_digit(self):
        """
        Verifica que el cambio de contraseña falla si la nueva contraseña no tiene un número.
        """
        data = {
            'old_password': 'OldPassword123',
            'new_password': 'NewPasswordABC'
        }
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password', response.data)
        self.assertIn('La nueva contraseña debe contener al menos un número.', response.data['new_password'])

    def test_change_password_new_password_no_uppercase(self):
        """
        Verifica que el cambio de contraseña falla si la nueva contraseña no tiene mayúscula.
        """
        data = {
            'old_password': 'OldPassword123',
            'new_password': 'newpassword123'
        }
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password', response.data)
        self.assertIn('La nueva contraseña debe contener al menos una letra mayúscula.', response.data['new_password'])

    def test_change_password_new_password_no_lowercase(self):
        """
        Verifica que el cambio de contraseña falla si la nueva contraseña no tiene minúscula.
        """
        data = {
            'old_password': 'OldPassword123',
            'new_password': 'NEWPASSWORD123'
        }
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password', response.data)
        self.assertIn('La nueva contraseña debe contener al menos una letra minúscula.', response.data['new_password'])

    def test_change_password_new_same_as_old(self):
        """
        Verifica que el cambio de contraseña falla si la nueva contraseña es igual a la antigua.
        """
        data = {
            'old_password': 'OldPassword123',
            'new_password': 'OldPassword123'
        }
        response = self.client.post(self.change_password_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password', response.data)
        self.assertIn('La nueva contraseña no puede ser igual a la anterior.', response.data['new_password'])

