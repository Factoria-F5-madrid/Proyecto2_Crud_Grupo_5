# categoria/models.py
from django.db import models

class Category(models.Model):
    # Django crea 'id' automáticamente, pero puedes explicitarlo si lo deseas
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True, verbose_name="Nombre de Categoría")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")

    class Meta:
        db_table = 'categories' # ¡CONFIRMA ESTO! Mapea a la tabla 'categories' de tu MySQL
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name