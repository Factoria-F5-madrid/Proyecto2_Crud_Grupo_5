from django.db import models
# Importamos los modelos Customer y Product de sus respectivas aplicaciones
from cliente.models import Customer
from prenda.models import Product
# Modelo para Pedidos (Órdenes de Compra)
class Order(models.Model):
    """
    Modelo que representa un pedido realizado por un cliente.
    Equivale a la tabla 'orders' en la base de datos.
    """
    # Relación uno a muchos con Customer: un pedido pertenece a un cliente
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name="Cliente")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del Pedido")

    class Meta:
        db_table = 'orders'
        verbose_name_plural = "Pedidos"
        verbose_name = "Pedido"
        indexes = [
            models.Index(fields=['customer']),
        ]

    def __str__(self):

        return f"Pedido #{self.id} de {self.customer.name} el {self.order_date.strftime('%Y-%m-%d')}"

# Modelo para Ítems del Pedido (Productos dentro de un Pedido)
class OrderItem(models.Model):
    """
    Modelo que representa un producto específico dentro de un pedido.
    Equivale a la tabla 'order_items' en la base de datos.
    """
    # Relación uno a muchos con Order: un item de pedido pertenece a un pedido
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Pedido")
    # Relación uno a muchos con Product: un item de pedido se refiere a un producto
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    quantity = models.IntegerField(default=1, verbose_name="Cantidad")

    class Meta:
        db_table = 'order_items'
        verbose_name_plural = "Ítems del Pedido"
        verbose_name = "Ítem del Pedido"
        unique_together = ('order', 'product') # Asegura que la combinación de pedido y producto sea única
        indexes = [
            models.Index(fields=['order']),
            models.Index(fields=['product']),
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product.name} en Pedido #{self.order.id}"