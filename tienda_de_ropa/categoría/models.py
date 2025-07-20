from django.db import models

# Modelo para Categorías de Productos


class Category(models.Model):
    """
    Modelo que representa una categoría de producto.
    Equivale a la tabla 'categories' en la base de datos.
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre")
    description = models.TextField(null=True, blank=True, verbose_name="Descripción")

    class Meta:
        db_table = 'categories'
        verbose_name_plural = "Categorías"
        verbose_name = "Categoría"

    def __str__(self):
        return self.name
