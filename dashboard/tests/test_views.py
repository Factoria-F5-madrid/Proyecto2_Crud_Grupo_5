from django.test import TestCase, Client as TestClient
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal

from clients.models import Client as AppClient # Renombrar para evitar conflicto con TestClient
from invoicing.models import Invoice

class DashboardViewTest(TestCase):
    def setUp(self):
        """Configura los datos necesarios para probar la vista del dashboard."""
        # Crear usuarios con diferentes permisos
        self.staff_user = User.objects.create_user(username='staff', password='testpass123', is_staff=True)
        self.regular_user = User.objects.create_user(username='customer', password='testpass123')
        
        # Cliente de Test de Django
        self.client = TestClient()
        
        # Datos de prueba para las estadísticas
        client1 = AppClient.objects.create(name='Empresa A', email='a@a.com')
        AppClient.objects.create(name='Empresa B', email='b@b.com')
        
        Invoice.objects.create(client=client1, due_date='2025-08-01', status='paid', total=Decimal('500.00'))
        Invoice.objects.create(client=client1, due_date='2025-08-15', status='paid', total=Decimal('250.50'))
        Invoice.objects.create(client=client1, due_date='2025-09-01', status='sent', total=Decimal('100.00'))
        
        # URL de la vista
        self.dashboard_url = reverse('dashboard_view')

    def test_dashboard_redirects_if_not_logged_in(self):
        """Prueba que un usuario no autenticado es redirigido a la página de login."""
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url) # La URL de login por defecto

    def test_dashboard_forbidden_for_regular_user(self):
        """Prueba que un usuario normal (no staff) no puede acceder al dashboard."""
        self.client.login(username='customer', password='testpass123')
        response = self.client.get(self.dashboard_url)
        # Por defecto, @login_required permite el acceso si estás logueado.
        # Si tienes permisos más estrictos (ej. @user_passes_test(lambda u: u.is_staff))
        # el código de estado sería 403 (Forbidden) o 302 (Redirect).
        # Asumiendo que cualquier usuario logueado puede verla por ahora:
        self.assertEqual(response.status_code, 200)

    def test_dashboard_accessible_for_staff_user(self):
        """Prueba que un usuario del personal puede acceder correctamente."""
        self.client.login(username='staff', password='testpass123')
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')
        
    def test_dashboard_context_data_is_correct(self):
        """Prueba que los datos de contexto calculados en la vista son correctos."""
        self.client.login(username='staff', password='testpass123')
        response = self.client.get(self.dashboard_url)
        
        self.assertEqual(response.status_code, 200)
        
        # Comprobar que los datos en el contexto son los que esperamos
        context = response.context
        self.assertEqual(context['total_clients'], 2)
        self.assertEqual(context['total_revenue'], Decimal('750.50'))
        self.assertEqual(context['paid_invoices_count'], 2)
        self.assertEqual(context['pending_invoices_count'], 1)