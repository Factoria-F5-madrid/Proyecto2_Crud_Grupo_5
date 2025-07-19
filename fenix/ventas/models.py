from django.db import models
from clientes.models import Cliente
from prendas.models import Prenda
from django.contrib.auth.models import User

class Venta(models.Model):
    fecha = models.DateTimeField(auto_now=True)
    cliente = models.ForeignKey(Cliente, related_name='ventas', on_delete=models.CASCADE)
    prenda = models.ForeignKey(Prenda, related_name='venta', on_delete=models.CASCADE)
    cantidad = models.PositiveBigIntegerField(default=1)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # Para saber qué usuaria registró la venta
    
    def __str__(self):
        return f"Venta {self.id} - {self.prenda.nombre} a {self.cliente.nombre} ({self.fecha})"

