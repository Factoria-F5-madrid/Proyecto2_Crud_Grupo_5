from django.contrib import admin
from .models import Service, ServiceCategory

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'category', 'price', 'tax_percentage', 'is_active')
    list_filter = ('is_active', 'category', 'tax_percentage')
    search_fields = ('name', 'code', 'description')
    ordering = ('name',)
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'code', 'description', 'is_active')
        }),
        ('Categorización', {
            'fields': ('category',)
        }),
        ('Precios e Impuestos', {
            'fields': ('price', 'tax_percentage')
        }),
    )