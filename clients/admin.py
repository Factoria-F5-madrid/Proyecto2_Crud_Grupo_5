from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'tax_id', 'city', 'email', 'phone', 'is_active')
    list_filter = ('is_active', 'city', 'province')
    search_fields = ('name', 'tax_id', 'email', 'contact_person')
    ordering = ('name',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'tax_id', 'is_active')
        }),
        ('Dirección', {
            'fields': ('address', 'postal_code', 'city', 'province', 'country')
        }),
        ('Contacto', {
            'fields': ('email', 'phone', 'contact_person')
        }),
        ('Notas', {
            'fields': ('notes',)
        }),
    )