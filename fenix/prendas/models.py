from django.db import models
from categorias.models import Categoria
    
class Prenda(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    Categoria = models.ForeignKey(Categoria, related_name='prendas', on_delete=models.SET_NULL, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveBigIntegerField(default=0)
    imagen = models.ImageField(upload_to='prendas', blank=True, null=True)
    
    def __str__(self):
        return self.nombre