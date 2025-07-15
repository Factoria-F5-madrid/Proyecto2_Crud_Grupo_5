from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from clients.models import Client
from invoicing.models import Invoice
from rest_framework.test import APITestCase

class DashboardAPITest(APITestCase):
    def setUp(self):
        """Crea datos de prueba para verificar las estadísticas del dashboard."""
        self.admin_user = User.objects.create_user('admin', 'pass', is_staff=True)
        self.client.force_authenticate(user=self.admin_user)
        
        # Crear clientes
        client1 = Client.objects.create(name='Cliente A', email='a@test.com', created_at=timezone.now())
        Client.objects.create(name='Cliente B', email='b@test.com', created_at=timezone.now() - timezone.timedelta(days=40))

        # Crear facturas
        Invoice.objects.create(client=client1, issue_date=timezone.now().date(), status='paid', total=Decimal('500.00'))
        Invoice.objects.create(client=client1, issue_date=timezone.now().date(), status='draft', total=Decimal('200.00'))
        
        # URL del dashboard (ajústala a tu proyecto)
        self.dashboard_stats_url = reverse('dashboard-stats')

    def test_get_dashboard_stats(self):
        """Test para verificar que las estadísticas del dashboard son correctas."""
        response = self.client.get(self.dashboard_stats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        # Verificar el número total de clientes
        self.assertEqual(data['total_clients'], 2)
        
        # Verificar el número de nuevos clientes en los últimos 30 días
        self.assertEqual(data['new_clients_last_30_days'], 1)

        # Verificar los ingresos totales (facturas pagadas)
        self.assertEqual(Decimal(data['total_revenue']), Decimal('500.00'))

        # Verificar el número de facturas pendientes/borrador
        self.assertEqual(data['pending_invoices'], 1)