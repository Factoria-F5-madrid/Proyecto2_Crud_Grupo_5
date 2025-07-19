from django.db import models
from clientes.models import Cliente
from prendas.models import Prenda
from django.conf import settings

class Venta(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    cliente = models.ForeignKey(Cliente, related_name='ventas', on_delete=models.CASCADE)
    prenda = models.ForeignKey(Prenda, related_name='venta', on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField(default=1)
    usuaria = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='ventas_registradas'
    )
    
    def __str__(self):
        return f"Venta {self.id} - {self.prenda.nombre} a {self.cliente.nombre} ({self.fecha})"

