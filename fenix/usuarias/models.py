from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

def usuaria_avatar_upload_path(instance, filename):
    """Generate upload path for usuaria avatars"""
    ext = filename.split('.')[-1]
    new_filename = f"usuaria_{instance.username}_{instance.id or 'new'}.{ext}"
    return f"usuarias/avatars/{new_filename}"

class Usuaria(models.Model):
    """
    Modelo para las usuarias del sistema.
    Representa a las empleadas o administradoras de la tienda.
    """
    ROLE_CHOICES = [
        ('ADMIN', 'Administradora'),
        ('EMPLOYEE', 'Empleada'),
        ('MANAGER', 'Gerente'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Activa'),
        ('INACTIVE', 'Inactiva'),
        ('SUSPENDED', 'Suspendida'),
    ]
    
    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Nombre de Usuario",
        help_text="Nombre único para identificar a la usuaria"
    )
    
    email = models.EmailField(
        unique=True,
        verbose_name="Correo Electrónico",
        help_text="Correo electrónico de la usuaria"
    )
    
    first_name = models.CharField(
        max_length=50,
        verbose_name="Nombre"
    )
    
    last_name = models.CharField(
        max_length=50,
        verbose_name="Apellido"
    )
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos."
    )
    
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        null=True,
        blank=True,
        verbose_name="Teléfono"
    )
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='EMPLOYEE',
        verbose_name="Rol"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ACTIVE',
        verbose_name="Estado"
    )
    
    avatar = models.ImageField(
        upload_to=usuaria_avatar_upload_path,
        null=True,
        blank=True,
        verbose_name="Avatar",
        help_text="Foto de perfil de la usuaria"
    )
    
    hire_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Contratación"
    )
    
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Salario"
    )
    
    address = models.TextField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Dirección"
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de Actualización"
    )
    
    class Meta:
        db_table = 'usuarias'
        verbose_name = "Usuaria"
        verbose_name_plural = "Usuarias"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"
    
    @property
    def full_name(self):
        """Devuelve el nombre completo de la usuaria"""
        return f"{self.first_name} {self.last_name}"
    
    def get_role_display_spanish(self):
        """Devuelve el nombre del rol en español"""
        role_dict = dict(self.ROLE_CHOICES)
        return role_dict.get(self.role, self.role)
