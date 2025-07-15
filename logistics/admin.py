from django.contrib import admin
from .models import Shipment
from core.models import Category

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    """
    Personalización del admin para el modelo Shipment.
    """
    list_display = (
        'shipment_code', 
        'client', 
        'recipient_name', 
        'packages',      # <-- Añadido (equivale a "Bultos")
        'weight_kg',     # <-- Añadido (equivale a "Kgs")
        'price',         # <-- Añadido (equivale a "Importe")
        'created_at', 
        'is_invoiced'
    )
    list_filter = ('is_invoiced', 'client')
    search_fields = ('shipment_code', 'client__legal_name', 'recipient_name')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Personalización del admin para el modelo Category.
    """ 
    search_fields = ('name',)