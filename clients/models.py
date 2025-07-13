from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nombre")
    tax_id = models.CharField(max_length=20, unique=True, verbose_name="NIF/CIF")
    address = models.CharField(max_length=255, verbose_name="Dirección")
    postal_code = models.CharField(max_length=10, verbose_name="Código Postal")
    city = models.CharField(max_length=100, verbose_name="Ciudad")
    province = models.CharField(max_length=100, verbose_name="Provincia")
    country = models.CharField(max_length=100, default="España", verbose_name="País")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    contact_person = models.CharField(max_length=200, blank=True, verbose_name="Persona de contacto")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    notes = models.TextField(blank=True, verbose_name="Notas")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['name']

    def __str__(self):
        return self.name