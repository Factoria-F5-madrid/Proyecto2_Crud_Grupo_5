from django.db import models
from categoría.models import Category
import os

def product_image_upload_path(instance, filename):
    """Generate upload path for product images"""
    # Extract file extension
    ext = filename.split('.')[-1]
    # Generate filename with product name and timestamp
    new_filename = f"product_{instance.name.replace(' ', '_')}_{instance.id or 'new'}.{ext}"
    return os.path.join('products', new_filename)

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
    # Campo de imagen para el producto
    image = models.ImageField(
        upload_to=product_image_upload_path,
        null=True,
        blank=True,
        verbose_name="Imagen del Producto",
        help_text="Sube una imagen del producto (formatos: JPG, PNG, WEBP)"
    )
    description = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="Descripción",
        help_text="Descripción detallada del producto"
    )
    # Relación uno a muchos con Category: un producto pertenece a una categoría
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='products', verbose_name="Categoría")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de Actualización")

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