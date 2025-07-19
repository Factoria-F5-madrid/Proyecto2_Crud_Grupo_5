from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuaria(AbstractUser):
    nombre = models.CharField(max_length=150)
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.email})"
    
    class Meta:
        verbose_name = "Datos de la Usuaria"
        verbose_name_plural = "Dato único de la Usuaria"
