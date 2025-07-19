from django.db import models
from categorias.models import Categoria
    
class Prenda(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    categoria = models.ForeignKey(Categoria, related_name='prendas', on_delete=models.SET_NULL, null=True)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveBigIntegerField(default=0)
    imagen = models.ImageField(upload_to='prendas', blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class Talla(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
    
class Color(models.Model):
    nombre = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nombre
    
class Variaciones(models.Model):
    prenda = models.ForeignKey(Prenda, on_delete=models.CASCADE, related_name='variaciones')
    talla = models.ForeignKey(Talla, on_delete=models.CASCADE)
    color = models.PositiveIntegerField(default=0)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    
    class Meta:
        unique_together = ('prenda', 'talla', 'color')
        
    def __str__(self):
        return f"{self.prenda.nombre} - {self.talla.nombre} - {self.color.nombre}"
    
class ImagenPrenda(models.Model):
    prenda = models.ForeignKey(Prenda, on_delete=models.CASCADE, related_name='imagenes')
    imagen = models.ImageField(upload_to='prendas/')
    es_principal = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.prenda.nombre} - Imagen principal: {self.es_principal}"
    