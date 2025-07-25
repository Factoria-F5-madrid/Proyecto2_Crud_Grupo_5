# compra/models.py
from django.db import models
from django.urls import reverse # ¡Asegúrate de que esta línea esté presente!
from decimal import Decimal
from cliente.models import Customer
from prenda.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('PROCESANDO', 'Procesando'),
        ('ENVIADO', 'Enviado'),
        ('COMPLETADO', 'Completado'),
        ('CANCELADO', 'Cancelado'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Cliente")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del Pedido")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name="Cantidad Total")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDIENTE', verbose_name="Estado")

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-order_date'] # Ordenar por fecha del pedido descendente

    def __str__(self):
        # Utiliza self.pk para el ID del pedido y self.customer.name para el nombre del cliente
        return f"Pedido #{self.pk} - Cliente: {self.customer.name} ({self.order_date.strftime('%Y-%m-%d')})"

    # API-only implementation - no HTML redirects needed
    # def get_absolute_url(self):
    #     return reverse('compra:order_detail', kwargs={'pk': self.pk})

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Pedido")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio Unitario")

    class Meta:
        verbose_name = "Ítem de Pedido"
        verbose_name_plural = "Ítems de Pedido"
        unique_together = ('order', 'product') # Un producto solo puede estar una vez en el mismo pedido

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Pedido #{self.order.pk})"

    @property
    def get_total(self):
        return self.quantity * self.price

# Importaciones para las señales
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Señal para actualizar el total del pedido cuando un OrderItem se guarda/crea
@receiver(post_save, sender=OrderItem)
def update_order_total_on_save(sender, instance, **kwargs):
    instance.order.total_amount = sum(item.get_total for item in instance.order.items.all())
    instance.order.save()

# Señal para actualizar el total del pedido cuando un OrderItem se elimina
@receiver(post_delete, sender=OrderItem)
def update_order_total_on_delete(sender, instance, **kwargs):
    instance.order.total_amount = sum(item.get_total for item in instance.order.items.all())
    instance.order.save()