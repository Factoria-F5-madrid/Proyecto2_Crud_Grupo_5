# config/tests.py

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import path, reverse # Asegúrate de que 'path' esté importado
from rest_framework.views import APIView # Importa APIView para la vista de prueba
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

# 1. Define la vista de prueba FUERA de la clase de tests
#    Esto permite que sea referenciada por las URLs temporales.
class TestProtectedView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Acceso concedido al recurso protegido."})

# 2. Define las URLs temporales a nivel de módulo
#    APITestCase buscará aquí las URLs cuando le digamos que use este módulo.
urlpatterns = [
    path('api/protected-resource/', TestProtectedView.as_view(), name='protected_resource_test'),
]


class JWTAuthenticationTests(APITestCase):
    # 3. Indica a APITestCase que use las URLs definidas en este mismo módulo
    #    '__name__' se refiere al nombre del módulo actual (config.tests).
    urls = __name__

    def setUp(self):
        # Crear un usuario de prueba que usaremos en los tests
        self.username = 'testuser'
        self.password = 'testpassword123'
        self.user = User.objects.create_user(username=self.username, password=self.password)

        # URLs de los endpoints JWT (estos sí deben estar en tu config/urls.py principal)
        self.token_obtain_url = reverse('token_obtain_pair')
        self.token_refresh_url = reverse('token_refresh')
        
        # La URL del recurso protegido ahora se resuelve usando las URLs definidas en este módulo
        self.protected_url = reverse('protected_resource_test') 

        # 4. ELIMINA EL BLOQUE DE CÓDIGO ANTERIOR QUE DEFINÍA TestProtectedView y self.urlpatterns
        #    dentro de setUp. Ya no es necesario aquí.

    def test_get_token_with_valid_credentials(self):
        """
        Verifica que se pueden obtener tokens con credenciales válidas.
        """
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(self.token_obtain_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data) # Verifica que hay un token de acceso
        self.assertIn('refresh', response.data) # Verifica que hay un token de refresco

        # Guarda los tokens para usarlos en otros tests
        self.access_token = response.data['access']
        self.refresh_token = response.data['refresh']

    def test_get_token_with_invalid_credentials(self):
        """
        Asegura que las credenciales incorrectas resultan en un error 401 Unauthorized.
        """
        data = {
            'username': 'wronguser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.token_obtain_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('detail', response.data) # Asegura que la clave 'detail' existe
        # Asigna error_message solo si 'detail' está presente
        if 'detail' in response.data:
            error_message = str(response.data['detail']).lower()
            self.assertIn('la combinación de credenciales no tiene una cuenta activa', error_message)
        else:
            # Si 'detail' no está presente, el test fallará aquí con un mensaje claro
            self.fail("La respuesta no contiene la clave 'detail'.")

    def test_access_protected_resource_without_token(self):
        """
        Verifica que no se puede acceder a un recurso protegido sin autenticación.
        """
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_resource_with_valid_token(self):
        """
        Verifica que se puede acceder a un recurso protegido con un token JWT válido.
        """
        # Primero, obtenemos un token válido
        self.test_get_token_with_valid_credentials() # Esto establecerá self.access_token

        # Luego, accedemos al recurso protegido con el token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Acceso concedido a tu recurso protegido real!")

    def test_access_protected_resource_with_invalid_token(self):
        """
        Verifica que no se puede acceder con un token JWT inválido.
        """
        invalid_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.invalid_signature"
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {invalid_token}')
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('code', response.data)
        self.assertEqual(response.data['code'], 'token_not_valid')

    def test_refresh_token(self):
        """
        Verifica que se puede refrescar un token de acceso usando el token de refresco.
        """
        # Primero, obtenemos un par de tokens
        self.test_get_token_with_valid_credentials()

        # Intentamos refrescar el token
        data = {'refresh': self.refresh_token}
        response = self.client.post(self.token_refresh_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data) # Debería devolver un nuevo token de acceso

        # Opcional: verifica que el nuevo token de acceso funciona
        new_access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {new_access_token}')
        response = self.client.get(self.protected_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_refresh_token_with_invalid_refresh_token(self):
        """
        Asegura que un token de refresco inválido no permite obtener un nuevo token de acceso.
        """
        data = {'refresh': 'invalid_refresh_token_string'}
        response = self.client.post(self.token_refresh_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('code', response.data)
        self.assertEqual(response.data['code'], 'token_not_valid')