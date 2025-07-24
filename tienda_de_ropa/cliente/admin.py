from django.contrib import admin
from .models import Customer  # ¡Aquí debe ser 'Customer'!

# Registra tu modelo aquí
admin.site.register(Customer)