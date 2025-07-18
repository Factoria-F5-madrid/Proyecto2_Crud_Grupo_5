from django.contrib import admin
from .models import Order, OrderItem # <-- ¡Asegúrate de que estas son las dos clases que importas!

# Registra tus modelos aquí
admin.site.register(Order)
admin.site.register(OrderItem)
