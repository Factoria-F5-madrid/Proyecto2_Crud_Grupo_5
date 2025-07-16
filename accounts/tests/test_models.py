from django.test import TestCase
from django.contrib.auth.models import User
from .models import Account

class AccountModelTest(TestCase):
    
    def setUp(self):
        """Crea un usuario para las pruebas, lo que debería activar la señal."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='test@example.com'
        )

    def test_account_is_created_for_new_user(self):
        """Prueba que se crea un perfil de Account automáticamente al crear un User."""
        self.assertTrue(Account.objects.filter(user=self.user).exists())
        self.assertEqual(self.user.account.user.username, 'testuser')

    def test_account_default_role_is_client(self):
        """Prueba que el rol por defecto de una nueva cuenta es 'client'."""
        account = Account.objects.get(user=self.user)
        self.assertEqual(account.role, Account.Role.CLIENT)

    def test_account_role_assignment(self):
        """Prueba que se puede cambiar y guardar un rol en la cuenta."""
        account = Account.objects.get(user=self.user)
        account.role = Account.Role.ADMIN
        account.save()
        
        updated_account = Account.objects.get(user=self.user)
        self.assertEqual(updated_account.role, Account.Role.ADMIN)

    def test_string_representation(self):
        """Prueba la representación en texto del modelo Account."""
        account = Account.objects.get(user=self.user)
        expected_str = f"{self.user.username} - {account.get_role_display()}"
        self.assertEqual(str(account), expected_str)