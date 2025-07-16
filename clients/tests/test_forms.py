from django.test import TestCase
from clients.forms import ClientForm  # Deberás ajustar esto según tu implementación
from clients.models import Client

class ClientFormTest(TestCase):
    def test_valid_form(self):
        """Test para verificar que el formulario es válido con datos correctos"""
        data = {
            'name': 'Cliente Formulario',
            'email': 'formulario@cliente.com',
            'phone': '911223344',
            'address': 'Dirección de prueba',
            'tax_id': 'A12345678',
            'is_active': True
        }
        form = ClientForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_email(self):
        """Test para verificar que el formulario es inválido con email incorrecto"""
        data = {
            'name': 'Cliente Email Inválido',
            'email': 'email-invalido',  # Email inválido
            'phone': '911223344',
            'is_active': True
        }
        form = ClientForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_duplicate_email(self):
        """Test para verificar que el formulario valida unicidad de email"""
        # Crear cliente con email existente
        Client.objects.create(
            name='Cliente Existente',
            email='duplicado@cliente.com',
            phone='900000000'
        )
        
        # Intentar crear otro cliente con el mismo email
        data = {
            'name': 'Cliente Duplicado',
            'email': 'duplicado@cliente.com',  # Email duplicado
            'phone': '911223344'
        }
        form = ClientForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)