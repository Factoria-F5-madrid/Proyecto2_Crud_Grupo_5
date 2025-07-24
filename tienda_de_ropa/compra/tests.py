from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, datetime
from decimal import Decimal

# Importa los modelos y formularios necesarios
from .models import Order, OrderItem
from prenda.models import Product
from cliente.models import Customer
from categoría.models import Category # <--- Asegúrate de que este import sea correcto para tu estructura
from .forms import OrderForm, OrderItemForm # Asegúrate de que OrderItemForm esté definido en forms.py


class OrderModelTest(TestCase):
    """
    Tests for the Order model.
    """
    def setUp(self):
        # Crear una categoría para los productos
        self.category = Category.objects.create(
            name="Ropa Casual",
            description="Prendas para uso diario"
        )
        # Crear un producto de prueba
        self.product = Product.objects.create(
            name="Camiseta de Algodón",
            size="M",
            color="Blanco",
            price=Decimal('15.99'),
            stock=100,
            category=self.category
        )
        # Crear un cliente de prueba
        self.customer = Customer.objects.create(
            name="Juan Perez",
            email="juan.perez@example.com",
            phone="123456789"
        )
        # Crear un pedido de prueba
        self.order = Order.objects.create(
            customer=self.customer,
            order_date=date(2023, 1, 15),
            total_amount=Decimal('0.00'), # Se actualizará automáticamente con OrderItem
            status='PENDIENTE'
        )

    def test_order_creation(self):
        """Test that an Order can be created."""
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(self.order.customer, self.customer)
        self.assertEqual(self.order.status, 'PENDIENTE')

    def test_order_str_representation(self):
        """Test the __str__ method of the Order model."""
        expected_str = f"Pedido #{self.order.pk} - Cliente: {self.customer.name} ({self.order.order_date.strftime('%Y-%m-%d')})"
        self.assertEqual(str(self.order), expected_str)


class OrderItemModelTest(TestCase):
    """
    Tests for the OrderItem model.
    """
    def setUp(self):
        # Crear una categoría para los productos
        self.category = Category.objects.create(
            name="Ropa Deportiva",
            description="Prendas para ejercicio"
        )
        # Crear un producto de prueba
        self.product = Product.objects.create(
            name="Pantalón Deportivo",
            size="L",
            color="Negro",
            price=Decimal('30.50'),
            stock=50,
            category=self.category
        )
        # Crear un cliente de prueba
        self.customer = Customer.objects.create(
            name="Maria Gomez",
            email="maria.gomez@example.com",
            phone="987654321"
        )
        # Crear un pedido de prueba
        self.order = Order.objects.create(
            customer=self.customer,
            order_date=date(2023, 2, 1),
            total_amount=Decimal('0.00'), # El total se inicializa en 0.00 y las señales lo actualizarán
            status='COMPLETADO'
        )
        # Crear un OrderItem de prueba
        # Esto disparará la señal post_save y actualizará order.total_amount
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=self.product.price # Precio del producto en el momento de la venta
        )
        # ¡IMPORTANTE! Después de crear o modificar un OrderItem en un test,
        # siempre refresca el objeto Order desde la base de datos para obtener el total_amount actualizado por la señal.
        self.order.refresh_from_db()


    def test_order_item_creation(self):
        """Test that an OrderItem can be created and associated with an Order and Product."""
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertEqual(self.order_item.price, Decimal('30.50'))
        # Verifica que el total del pedido se actualizó automáticamente por la señal
        self.assertEqual(self.order.total_amount, Decimal('61.00')) # 2 * 30.50

    def test_order_item_str_representation(self):
        """Test the __str__ method of the OrderItem model."""
        expected_str = f"2 x Pantalón Deportivo (Pedido #{self.order.pk})"
        self.assertEqual(str(self.order_item), expected_str)

    def test_order_total_amount_calculation(self):
        """Test that total_amount is correctly calculated based on order items."""
        # En este punto, order.total_amount ya es 61.00 por el OrderItem creado en setUp
        self.assertEqual(self.order.total_amount, Decimal('61.00'))

        # Añadir otro item para ver si suma
        product2 = Product.objects.create(
            name="Calcetines", size="U", color="Gris", price=Decimal('5.00'), stock=200, category=self.category
        )
        # Crear un nuevo OrderItem. Esto disparará la señal y recalculará el total del Order.
        OrderItem.objects.create(
            order=self.order, product=product2, quantity=4, price=product2.price
        )
        # Recargar el pedido de la base de datos para obtener el total_amount actualizado por la señal
        self.order.refresh_from_db()
        # total_amount debería ser 61.00 (del primer item) + 20.00 (4*5.00 del segundo item) = 81.00
        self.assertEqual(self.order.total_amount, Decimal('81.00'))


class OrderViewTest(TestCase):
    """
    Tests for the Order views.
    """
    def setUp(self):
        self.client = Client() # El cliente de prueba para hacer peticiones HTTP
        # Crear objetos de prueba necesarios para las vistas
        self.category = Category.objects.create(name="Ropa", description="General")
        self.product = Product.objects.create(
            name="Zapatos", size="42", color="Negro", price=Decimal('50.00'), stock=50, category=self.category
        )
        self.customer = Customer.objects.create(
            name="Ana Lopez",
            email="ana.lopez@example.com",
            phone="111222333"
        )
        self.order = Order.objects.create(
            customer=self.customer, order_date=date(2024, 5, 20), status='PENDIENTE', total_amount=Decimal('0.00')
        )
        # Crear un OrderItem para que el pedido tenga un total_amount > 0
        # Esto disparará la señal y actualizará order.total_amount
        self.order_item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1, price=self.product.price
        )
        self.order.refresh_from_db() # Refrescar para obtener el total actualizado por la señal

        # URLs con sus nombres definidos en compra/urls.py
        self.list_url = reverse('compra:order_list')
        self.detail_url = reverse('compra:order_detail', args=[self.order.pk])
        self.create_url = reverse('compra:order_create')
        self.update_url = reverse('compra:order_update', args=[self.order.pk])
        self.delete_url = reverse('compra:order_delete', args=[self.order.pk])

    def test_order_list_view(self):
        """Test that the order list view is accessible and displays orders."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200) # Verifica que la página carga correctamente
        self.assertTemplateUsed(response, 'compra/order_list.html') # Verifica que usa la plantilla correcta
        self.assertContains(response, self.order.customer.name)

    def test_order_detail_view(self):
        """Test that the order detail view is accessible and displays order details."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compra/order_detail.html')
        self.assertContains(response, self.order.customer.name)
        self.assertContains(response, self.product.name) # Verifica que el producto del OrderItem aparece

    def test_order_create_view_get(self):
        """Test that the order create view loads correctly (GET request)."""
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compra/order_form.html')
        self.assertIsInstance(response.context['form'], OrderForm) # Verifica que el formulario está en el contexto

    def test_order_create_view_post_valid_data(self):
        """Test that a new order can be created via POST request with valid data."""
        initial_order_count = Order.objects.count()
        response = self.client.post(self.create_url, {
            'customer': self.customer.pk, # Pk del cliente existente
            'order_date': '2024-07-23T10:00', # Formato para DateTimeInput
            'total_amount': '0.00', # Puedes poner 0.00 aquí, la señal lo ajustará si se añaden ítems
            'status': 'PROCESANDO'
        })
        self.assertEqual(response.status_code, 302) # Debería redirigir después de crear
        self.assertEqual(Order.objects.count(), initial_order_count + 1)
        # Se puede añadir un assert para verificar si el objeto recién creado tiene el customer correcto, etc.
        new_order = Order.objects.latest('order_date') # Obtener el último pedido creado
        self.assertEqual(new_order.customer, self.customer)
        # Ya no necesitamos verificar la redirección aquí porque get_absolute_url
        # del modelo se encarga y el test de update ya lo verifica.


    def test_order_create_view_post_invalid_data(self):
        """Test that new order is not created with invalid data (POST request)."""
        initial_order_count = Order.objects.count()
        response = self.client.post(self.create_url, {
            'customer': '', # Datos inválidos (cliente vacío si es requerido)
            'order_date': 'invalid-date',
            'total_amount': 'abc', # Dato inválido para total_amount
            'status': 'PENDIENTE'
        })
        self.assertEqual(response.status_code, 200) # Debería renderizar el formulario de nuevo con errores
        self.assertTemplateUsed(response, 'compra/order_form.html')
        self.assertEqual(Order.objects.count(), initial_order_count) # No se debe crear un nuevo pedido
        self.assertContains(response, "This field is required.") # CAMBIO AQUÍ: Mensaje de error para customer
        self.assertContains(response, "Enter a number.") # Mensaje de error para total_amount si es 'abc'

    def test_order_update_view_get(self):
        """Test that the order update view loads correctly (GET request)."""
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compra/order_form.html')
        self.assertEqual(response.context['form'].instance, self.order) # Verifica que el formulario está precargado

    def test_order_update_view_post_valid_data(self):
        """Test that an existing order can be updated via POST request with valid data."""
        new_status = 'ENVIADO'
        response = self.client.post(self.update_url, {
            'customer': self.customer.pk,
            'order_date': '2024-05-20T12:00', # Misma fecha, o nueva si se desea
            'total_amount': str(self.order.total_amount), # Mandar el valor actual como string
            'status': new_status
        })
        self.assertEqual(response.status_code, 302) # Debería redirigir
        self.order.refresh_from_db() # Recargar el objeto desde la DB para ver los cambios
        self.assertEqual(self.order.status, new_status)
        self.assertRedirects(response, self.detail_url) # Verificar que redirige al detalle (ahora sí, por get_absolute_url)

    def test_order_update_view_post_invalid_data(self):
        """Test that an existing order is not updated with invalid data (POST request)."""
        original_status = self.order.status
        response = self.client.post(self.update_url, {
            'customer': '', # Datos inválidos
            'order_date': 'invalid-date',
            'total_amount': 'invalid_decimal', # Dato inválido
            'status': 'INVALID_STATUS' # Esto sigue siendo inválido, está bien para este test
        })
        self.assertEqual(response.status_code, 200) # Debería renderizar el formulario de nuevo
        self.assertTemplateUsed(response, 'compra/order_form.html')
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, original_status) # El estado no debe haber cambiado
        self.assertContains(response, "This field is required.") # CAMBIO AQUÍ
        self.assertContains(response, "Enter a number.")
        self.assertContains(response, "Select a valid choice. INVALID_STATUS is not one of the available choices.")

    def test_order_delete_view_get(self):
        """Test that the order delete confirmation page loads correctly (GET request)."""
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'compra/order_confirm_delete.html')
        self.assertContains(response, "Estás seguro de que quieres eliminar el pedido")

    def test_order_delete_view_post(self):
        """Test that an order can be deleted via POST request."""
        initial_order_count = Order.objects.count()
        response = self.client.post(self.delete_url)
        self.assertEqual(response.status_code, 302) # Debería redirigir
        self.assertEqual(Order.objects.count(), initial_order_count - 1) # El pedido debe haber sido eliminado
        self.assertRedirects(response, self.list_url) # Verificar que redirige a la lista