from django.db import models

# Modelo para Clientes
class Customer(models.Model):
    """
    Modelo que representa un cliente.
    Equivale a la tabla 'customers' en la base de datos.
    """
    name = models.CharField(max_length=100, verbose_name="Nombre del Cliente")
    email = models.EmailField(max_length=100, unique=True, verbose_name="Correo Electrónico")
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name="Teléfono")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    class Meta:
        db_table = 'customers'
        verbose_name_plural = "Clientes"
        verbose_name = "Cliente"
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.name