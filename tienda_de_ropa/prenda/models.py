from django.db import models
from categoría.models import Category

# Modelo para Productos
class Product(models.Model):
    """
    Modelo que representa un producto de la tienda de ropa.
    Equivale a la tabla 'products' en la base de datos.
    """
    name = models.CharField(max_length=100, verbose_name="Nombre del Producto")
    size = models.CharField(max_length=10, null=True, blank=True, verbose_name="Talla")
    color = models.CharField(max_length=30, null=True, blank=True, verbose_name="Color")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    stock = models.IntegerField(default=0, verbose_name="Stock Disponible")
    # Relación uno a muchos con Category: un producto pertenece a una categoría
    # Usamos Category directamente porque la importamos.
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="Categoría")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")

    class Meta:
        db_table = 'products'
        verbose_name_plural = "Productos"
        verbose_name = "Producto"
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} ({self.size}, {self.color})"