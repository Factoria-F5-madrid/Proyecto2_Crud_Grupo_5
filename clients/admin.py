from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('legal_name', 'tax_id', 'get_location', 'email', 'phone', 'is_active')
    list_filter = ('is_active', 'location__province')
    search_fields = ('legal_name', 'tax_id', 'email', 'contact_person')
    ordering = ('legal_name',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('legal_name', 'tax_id', 'is_active')
        }),
        ('Dirección', {
            'fields': ('address', 'postal_code','location__province', 'country')
        }),
        ('Contacto', {
            'fields': ('email', 'phone', 'contact_person')
        }),
        ('Notas', {
            'fields': ('notes',)
        }),
    )
    
    @admin.display(description='Location', ordering='location__name')
    def get_location(self, obj):
        """Muestra el nombre de la ubicación en la lista del admin."""
        if obj.location:
            return obj.location.name
        return "N/A"