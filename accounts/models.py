from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Account(models.Model):
    """
    Extiende el modelo User de Django para añadir roles.
    """
    class Role(models.TextChoices):
        ADMIN = 'admin', 'Administrador'
        STAFF = 'staff', 'Personal'
        CLIENT = 'client', 'Cliente'

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.CLIENT)

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"

# Esta señal crea automáticamente un 'Account' cada vez que se crea un 'User'
@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)